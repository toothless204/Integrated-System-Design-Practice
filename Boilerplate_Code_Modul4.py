import pandas as pd
import streamlit as st
import pyodbc
import time
from streamlit_extras.stylable_container import stylable_container

# =======================================
# Konfigurasi Database & Skema (ERD Standar)
# =======================================

#Database
DB_NAME = "PPSTaSIK" #Input Database
SERVER_NAME = "ADJI\SQLEXPRESS" #Input Detail Server

# Nama tabel
TBL_PROCESS_REQUEST         = "Process_Request" #Input Table Process Request
TBL_PROCESS_ACTUAL          = "Process_Aktual" #Input Table Process Actual
TBL_OPERATOR                = "Operator" #Input Table Operator
TBL_MATERIAL                = "Material" #Input Table Material
TBL_MATERIAL_CONSUMED_REQ   = "Material_Consumed_Request" #Input Table Material Request
TBL_EQUIPMENT               = "Equipment" #Input Table Equipment
TBL_MATERIAL_CONSUMED_ACTUAL = "Material_Consumed_Actual" #Input Table Material Consumed Actual

# Nama kolom pada tabel OPERATOR
COL_OPERATOR_NAME           = "Nama_Operator" #Input kolom Nama Operator

# Nama kolom pada tabel MATERIAL
COL_MATERIAL_ID             = "Material_ID" #Input kolom Material ID
COL_MATERIAL_NAME           = "Material_Name" #Input kolom Nama Material

# Nama kolom pada tabel MATERIAL CONSUMED REQUEST
COL_MATERIAL_REQ_ID         = "MaterialReq_ID" #Input kolom Material Request ID

# Nama kolom pada tabel MATERIAL CONSUMED ACTUAL
COL_MATERIAL_ACT_ID         = "MaterialAct_ID"  #Input Kolom Material Consumed Actual ID
COL_QUANTITY_ACTUAL         = "Quantity_Act" #Input Quantity Actual 


# Nama kolom pada tabel EQUIPMENT_
COL_EQUIPMENT_ID            = "Equipment_ID" #Input kolom Equipment ID
COL_EQUIPMENT_NAME          = "Equipment_Name" #Input kolom Nama Equipment


# Nama kolom pada tabel PROCESS_REQUEST
COL_PROC_REQ_ID             = "ProcReq_ID" #Input Kolom Process Request ID
COL_PROCESS_NAME            = "Process_Name" #Input Kolom Process Request Name
COL_PROCESS_TIME_REQ        = "ProcessTime_Req" #Input Kolom Process Request Time
COL_OPERATOR_ID             = "Operator_ID" #Input kolom Operator ID
COL_PART_NAME               = "Part_Name" #Input kolom Part Name

# Nama kolom pada tabel PROCESS_ACTUAL
COL_PROCESS_START_TIME      = "Process_StartTime" #Input kolom Process Start Time
COL_PROCESS_END_TIME        = "Process_EndTime" #Input kolom Process End time
COL_WORK_STATUS             = "Work_Status" #Input kolom Work Status
COL_DEFECTS                 = "Defect" #Input kolom Defect
COL_DURATION_ACTUAL         = "Duration" #Input Kolom Durasi Aktual
COL_CUTSPEED                = "Cutting_Speed" #Input Kolom Cutting Speed
COL_SPINDLESPEED            = "SpindleSpeed" #Input Kolom Spindle Speed
COL_FEEDRATE                = "Feed_Rate" #Input Kolom Feed Rate
COL_DOC                     = "Depth_Of_Cut" #Input Kolom Depth of Cut

# Alias (alias display pada data frame/layar)
ALIAS_REQUEST_ID            = "Request ID" #JANGAN DIUBAH
ALIAS_PROCESS               = "Process" #JANGAN DIUBAH
ALIAS_START_TIME            = "Start Time" #JANGAN DIUBAH
ALIAS_END_TIME              = "End Time" #JANGAN DIUBAH


# =======================================
# Sampai sini saja editnya, setelah komentar ini bisa didiamkan saja.
# =======================================

# =======================================
# Styling untuk tampilan table dan judul
# =======================================
st.markdown(
    """
    <style>
    
    /* Center-align the table */
    .stDataFrame {
        margin: 0 auto;
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =======================================
# Inisialisasi Session State
# =======================================
if "progress" not in st.session_state:
    st.session_state.progress = 0
if "status" not in st.session_state:
    st.session_state.status = "Idle"
if "processing" not in st.session_state:
    st.session_state.processing = False
if 'starttime' not in st.session_state:
    st.session_state.starttime = time.strftime("%H:%M:%S")
if 'finishtime' not in st.session_state:
    st.session_state.finishtime = time.strftime("%H:%M:%S")

# =======================================
# Fungsi Koneksi Database
# =======================================
def create_connection():
    """Buat koneksi ke database SQL Server."""
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        f'SERVER={SERVER_NAME};'  # Ganti dengan server Anda
        f'DATABASE={DB_NAME};'    # Ganti dengan nama database Anda
        'Trusted_Connection=yes;'
    )
    return conn

# =======================================
# Fungsi-fungsi untuk Query Data
# =======================================
def fetch_data():
    """Fetch nama-nama tabel dari database."""
    conn = create_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES;")
        tables = cursor.fetchall()
        conn.close()
        return tables if tables else []
    except Exception as e:
        st.error(f"Error fetching tables: {e}")
        return []

def fetch_table_data(table_name):
    """Fetch semua data dari tabel tertentu."""
    conn = create_connection()
    if conn is None:
        return []
    try:
        query = f"SELECT * FROM [{table_name}];"
        df = pd.read_sql(query, conn)
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data from {table_name}: {e}")
        return pd.DataFrame()

def MainTableQuery(processRequest_table):
    conn = create_connection()
    if conn is None:
        st.error("Koneksi ke database gagal.")
        return pd.DataFrame()
    try:
        # Menggunakan variabel untuk nama tabel dan kolom
        query = f"""
                SELECT 
                    [{processRequest_table}].{COL_PROC_REQ_ID} AS [{ALIAS_REQUEST_ID}],
                    [{processRequest_table}].{COL_PROCESS_NAME} AS [{ALIAS_PROCESS}],
                    pa.{COL_PROCESS_START_TIME} AS [{ALIAS_START_TIME}],
                    pa.{COL_PROCESS_END_TIME} AS [{ALIAS_END_TIME}],
                    pa.{COL_DEFECTS} As Defect,
                    pa.{COL_WORK_STATUS} AS Status
                FROM {TBL_PROCESS_REQUEST} [{processRequest_table}]
                JOIN {TBL_PROCESS_ACTUAL} pa 
                    ON [{processRequest_table}].{COL_PROC_REQ_ID} = pa.{COL_PROC_REQ_ID};
            """

        df = pd.read_sql(query, conn)
        # Format waktu jika data tidak kosong
        if not df.empty:
            df[ALIAS_START_TIME] = pd.to_datetime(df[ALIAS_START_TIME]).dt.strftime('%H:%M:%S')
            df[ALIAS_END_TIME] = pd.to_datetime(df[ALIAS_END_TIME]).dt.strftime('%H:%M:%S')
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data from {processRequest_table}: {e}")
        return pd.DataFrame()

def OperatorQuery(processActual_table, ID):
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        query = f"""
            SELECT [{COL_OPERATOR_NAME}]
            FROM {TBL_OPERATOR}
            JOIN [{processActual_table}] 
                ON {TBL_OPERATOR}.{COL_OPERATOR_ID} = [{processActual_table}].{COL_OPERATOR_ID}
            WHERE {COL_PROC_REQ_ID} = '{ID}';
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching operator data: {e}")
        return pd.DataFrame()

def StatusQuery(processActual_table, ID):
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        query = f"""
            SELECT {COL_WORK_STATUS}
            FROM [{processActual_table}]
            WHERE {COL_PROC_REQ_ID} = '{ID}';
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching status: {e}")
        return pd.DataFrame()

def ActualDurationQuery(processActual_table, ID):
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        query = f"""
            SELECT {COL_DURATION_ACTUAL}
            FROM [{processActual_table}]
            WHERE {COL_PROC_REQ_ID} = '{ID}';
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching status: {e}")
        return pd.DataFrame()

def CuttingSpeedQuery(processActual_table, ID):
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        query = f"""
            SELECT {COL_CUTSPEED}
            FROM [{processActual_table}]
            WHERE {COL_PROC_REQ_ID} = '{ID}';
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching status: {e}")
        return pd.DataFrame()

def SpindleSpeedQuery(processActual_table, ID):
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        query = f"""
            SELECT {COL_SPINDLESPEED}
            FROM [{processActual_table}]
            WHERE {COL_PROC_REQ_ID} = '{ID}';
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching status: {e}")
        return pd.DataFrame()

def FeedRateQuery(processActual_table, ID):
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        query = f"""
            SELECT {COL_FEEDRATE}
            FROM [{processActual_table}]
            WHERE {COL_PROC_REQ_ID} = '{ID}';
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching status: {e}")
        return pd.DataFrame()

def DoCQuery(processActual_table, ID):
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        query = f"""
            SELECT {COL_DOC}
            FROM [{processActual_table}]
            WHERE {COL_PROC_REQ_ID} = '{ID}';
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching status: {e}")
        return pd.DataFrame()

def StartTimeQuery(processRequest_table, ID):
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        query = f"""
            SELECT {COL_PROCESS_TIME_REQ}
            FROM [{processRequest_table}]
            WHERE {COL_PROC_REQ_ID} = '{ID}';
        """
        df = pd.read_sql(query, conn)
        if not df.empty:
            df[COL_PROCESS_TIME_REQ] = pd.to_datetime(df[COL_PROCESS_TIME_REQ]).dt.strftime('%H:%M:%S')
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching duration: {e}")
        return pd.DataFrame()

def MaterialQuery(processRequest_table, ID):
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        query = f"""
            SELECT {COL_MATERIAL_NAME}
            FROM {TBL_MATERIAL}
            INNER JOIN {TBL_MATERIAL_CONSUMED_REQ} 
                ON {TBL_MATERIAL}.{COL_MATERIAL_ID} = {TBL_MATERIAL_CONSUMED_REQ}.{COL_MATERIAL_ID}
            JOIN {TBL_PROCESS_REQUEST} 
                ON {TBL_PROCESS_REQUEST}.{COL_MATERIAL_REQ_ID} = {TBL_MATERIAL_CONSUMED_REQ}.{COL_MATERIAL_REQ_ID}
            WHERE {COL_PROC_REQ_ID} = '{ID}';
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching material: {e}")
        return pd.DataFrame()

def ProcessQuery(processRequest_table, ID):
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        query = f"""
            SELECT {COL_PROCESS_NAME}
            FROM [{processRequest_table}]
            WHERE {COL_PROC_REQ_ID} = '{ID}';
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching process info: {e}")
        return pd.DataFrame()

def PartQuery(processRequest_table, ID):
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        query = f"""
            SELECT {COL_PART_NAME}
            FROM [{processRequest_table}]
            WHERE {COL_PROC_REQ_ID} = '{ID}';
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching part info: {e}")
        return pd.DataFrame()

def MachineQuery(processActual_table, ID):
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        query = f"""
            SELECT {COL_EQUIPMENT_NAME}
            FROM {TBL_EQUIPMENT}
            JOIN [{processActual_table}]
                ON {TBL_EQUIPMENT}.{COL_EQUIPMENT_ID} = [{processActual_table}].{COL_EQUIPMENT_ID}
            WHERE {COL_PROC_REQ_ID} = '{ID}';
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching machine info: {e}")
        return pd.DataFrame()

def alterstatus(processActual_table, status, ID):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"""
        UPDATE [{processActual_table}]
        SET {COL_WORK_STATUS} = '{status}'
        WHERE {COL_PROC_REQ_ID} = '{ID}';
    """
    cursor.execute(query)
    conn.commit()
    conn.close()

def start_process(processActual_table, ID, starttime):
    conn = create_connection()
    cursor = conn.cursor()
    # Ubah status menjadi 'ONGOING' dan set waktu mulai
    query = f"""
        UPDATE [{processActual_table}]
        SET {COL_WORK_STATUS} = 'On Going',
            {COL_PROCESS_START_TIME} = '{starttime}'
        WHERE {COL_PROC_REQ_ID} = '{ID}';
    """
    cursor.execute(query)
    conn.commit()
    conn.close()

def abort_process(processActual_table, ID):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"""
        UPDATE [{processActual_table}]
        SET {COL_WORK_STATUS} = 'NOT STARTED',
            {COL_PROCESS_START_TIME} = NULL
        WHERE {COL_PROC_REQ_ID} = '{ID}';
    """
    cursor.execute(query)
    conn.commit()
    conn.close()

def update_defect(processActual_table, ID, defectstatus):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"""
        UPDATE [{processActual_table}]
        SET {COL_DEFECTS} = '{defectstatus}'
        WHERE {COL_PROC_REQ_ID} = '{ID}';
    """
    cursor.execute(query)
    conn.commit()
    conn.close()

def MaterialUsedQuery(tblmat, ID):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"""
        SELECT [{COL_MATERIAL_NAME}] FROM [{tblmat}]
        JOIN [{TBL_MATERIAL_CONSUMED_REQ}] mcr 
        ON [{tblmat}].[{COL_MATERIAL_ID}] = mcr.[{COL_MATERIAL_ID}]
        JOIN [{TBL_MATERIAL_CONSUMED_ACTUAL}] mca
        ON mcr.[{COL_MATERIAL_REQ_ID}] = mca.[{COL_MATERIAL_REQ_ID}]
        JOIN [{TBL_PROCESS_ACTUAL}] pa
        ON mca.[{COL_MATERIAL_ACT_ID}] = pa.[{COL_MATERIAL_ACT_ID}]
        WHERE pa.{COL_PROC_REQ_ID} = '{ID}' ;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df if not df.empty else pd.DataFrame()

def MaterialConsumedQuery(TBLMC, ID):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"""
        SELECT [{COL_QUANTITY_ACTUAL}] FROM [{TBLMC}]
        JOIN [{TBL_PROCESS_ACTUAL}] pa
        ON [{TBLMC}].[{COL_MATERIAL_ACT_ID}] = pa.[{COL_MATERIAL_ACT_ID}]
        WHERE pa.{COL_PROC_REQ_ID} = '{ID}' ;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df if not df.empty else pd.DataFrame()

# Fungsi callback untuk status defect
def defect_detected():
    st.session_state["defectCheck"] = True
    st.session_state["processing"] = False
    st.session_state["progress"] = 0
    st.session_state["startButton"] = True
    st.session_state["abortButton"] = True
    update_defect(TBL_PROCESS_ACTUAL, selbox, 'FALSE')

def no_defect_detected():
    st.session_state["defectCheck"] = True
    st.session_state["processing"] = False
    st.session_state["progress"] = 0
    st.session_state["startButton"] = True
    st.session_state["abortButton"] = True
    update_defect(TBL_PROCESS_ACTUAL, selbox, 'TRUE')

# =======================================
# Fungsi Styling untuk table utama
# =======================================
def highlight_status(val):
    color = ''
    if val == 'Finish':
        color = 'background-color: green; color: white'
    elif val == 'NOT STARTED':
        color = 'background-color: red; color: white'
    elif val == 'On Going':
        color = 'background-color: orange; color: black'
    return color

# =======================================
# Tampilan UI menggunakan Streamlit
# =======================================
st.markdown("<h1 style='text-align: center; color: White;'>PRODUCTION INFORMATION SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: White;'>PT PPST MANUFACTURING</h5>", unsafe_allow_html=True)

# Misalnya, untuk query table utama kita gunakan tabel proses aktual
# Di sini kita passing nama tabel dari konfigurasi (misalnya, TBL_PROCESS_ACTUAL) sebagai parameter
df = MainTableQuery(TBL_PROCESS_ACTUAL)

# Ubah nama kolom pada dataframe untuk tampilan
display_df = df.rename(columns={
    ALIAS_REQUEST_ID: ALIAS_REQUEST_ID,
    ALIAS_PROCESS: ALIAS_PROCESS,
    ALIAS_START_TIME: ALIAS_START_TIME,
    ALIAS_END_TIME: ALIAS_END_TIME,
})

# Terapkan warna berdasarkan status
styled_df = display_df.style.applymap(highlight_status, subset=['Status'])

# Tampilkan dataframe
st.dataframe(styled_df, use_container_width=True)

selectable_row = display_df[ALIAS_REQUEST_ID].tolist()

# Session State untuk tombol Start
if st.session_state.get("startButton", True):
    selbox = st.selectbox("Select Process Request", selectable_row, key="selbox")

    if selbox:
        #Info Untuk Request
        ProcessInfo  = ProcessQuery(TBL_PROCESS_REQUEST, selbox)
        PartInfo     = PartQuery(TBL_PROCESS_REQUEST, selbox)
        MachineInfo  = MachineQuery(TBL_PROCESS_ACTUAL, selbox)
        OperatorInfo = OperatorQuery(TBL_PROCESS_ACTUAL, selbox)
        MaterialInfo = MaterialQuery(TBL_PROCESS_REQUEST, selbox)
        StartTimeInfo = StartTimeQuery(TBL_PROCESS_REQUEST, selbox)
        StatusInfo   = StatusQuery(TBL_PROCESS_ACTUAL, selbox)
        Warnastatus  = StatusInfo[COL_WORK_STATUS].iloc[0]  # Contoh: "Done", "Ongoing", "Pending"
        

    #Info Untuk report
    container = st.container()
    # Tentukan bayangan berdasarkan status
    shadow_color = {
        "Finish": "0 10px 20px rgba(0, 200, 100, 0.5)",      # Hijau
        "NOT STARTED": "0 10px 20px rgba(255, 0, 0, 0.4)"      # Merah
    }.get(Warnastatus, "0 30px 50px rgba(0,0,0,0.05)")  # Default bayangan
    
    # Container untuk menampilkan detail Process Request
    container.write(
        f"""
        <div style="
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: {shadow_color};
            transition: transform 0.2s;
            color: black">
            <h3 style="text-align: center;"><strong>PROCESS REQUEST</strong></h3>
            <p style="margin: 5px 0;"><strong>Process</strong> : {ProcessInfo[COL_PROCESS_NAME].iloc[0]}</p>
            <p style="margin: 5px 0;"><strong>Part</strong> : {PartInfo[COL_PART_NAME].iloc[0]}</p>
            <p style="margin: 5px 0;"><strong>Operator</strong> : {OperatorInfo[COL_OPERATOR_NAME].iloc[0]}</p>
            <p style="margin: 5px 0;"><strong>Material</strong> : {MaterialInfo[COL_MATERIAL_NAME].iloc[0]}</p>
            <p style="margin: 5px 0;"><strong>Requested Starting Time</strong> : {StartTimeInfo[COL_PROCESS_TIME_REQ].iloc[0]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Input waktu mulai
    timestart = st.time_input("Enter Starting Time", key='timestart')

    # Tombol START (Hijau)
    with stylable_container(
        key="start_button_container",
        css_styles="""
            button {
                background-color: #4CAF50;
                color: white;
                padding: 14px;
                font-size: 18px;
                border: none;
                border-radius: 12px;
                width: 100%;
                margin-top: 10px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
        """,
    ):
        start = st.button("Start", key="start_button_container")

    if start:
            start_process(TBL_PROCESS_ACTUAL, selbox, timestart.strftime("%H:%M"))
            st.session_state["processing"] = True
            st.session_state["progress"] = 0
            st.session_state["defectCheck"] = False
            st.session_state["Finished"] = False
            st.session_state["startButton"] = False
            st.session_state["abortButton"] = True
            st.rerun()
else:
    selbox = st.selectbox("Select Process Request", selectable_row, index=selectable_row.index(st.session_state.selbox), disabled=True, key="selbox")
    timestart = st.time_input("Enter Starting Time", value=st.session_state.timestart, disabled=True, key="timestart")

if st.session_state.get("processing", False):
    progress_bar = st.progress(st.session_state["progress"])

    if st.session_state.get("abortButton", False):
        with stylable_container(
            key="abort_button_container",
            css_styles="""
                button {
                    background-color: #f44336;
                    color: white;
                    padding: 14px;
                    font-size: 18px;
                    border: none;
                    border-radius: 12px;
                    width: 100%;
                    margin-top: 10px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #d32f2f;
                }
            """,
        ):
            abort_clicked = st.button("🛑 Abort", key="abort_btn")

        if abort_clicked:
            abort_process(TBL_PROCESS_ACTUAL, selbox)
            st.session_state["processing"] = False
            st.session_state["progress"] = 0
            st.session_state["defectCheck"] = False
            st.session_state["Finished"] = False
            st.session_state["startButton"] = True
            st.session_state["abortButton"] = True
            st.error("Process Aborted!")
            abortplaceholder = st.empty()
            abortplaceholder.write("Aborting Process...")
            time.sleep(3)
            abortplaceholder.empty()
            st.rerun()

    if st.session_state["progress"] < 100:
        time.sleep(1)
        st.session_state["progress"] += 25
        st.rerun()
    else:
        st.session_state["abortButton"] = False
        if st.session_state.get("Finished", False): 
            st.session_state["processing"] = False
            st.success("Proses selesai!")
            gen_placeholder = st.empty()
            gen_placeholder.write("Generating Report...")
            time.sleep(3)
            ActualDurationInfo = ActualDurationQuery(TBL_PROCESS_ACTUAL, selbox)
            MaterialUsedInfo = MaterialUsedQuery(TBL_MATERIAL, selbox)
            MaterialConsumedInfo = MaterialConsumedQuery(TBL_MATERIAL_CONSUMED_ACTUAL, selbox)
            #QuantityProducedInfo = QuantityProducedQuery(TBL_PROCESS_REQUEST, selbox)
            CuttingSpeedInfo = CuttingSpeedQuery(TBL_PROCESS_REQUEST, selbox)
            FeedRateInfo = FeedRateQuery(TBL_PROCESS_REQUEST, selbox)
            SpindleSpeedInfo = SpindleSpeedQuery(TBL_PROCESS_REQUEST, selbox)
            DoCInfo = DoCQuery(TBL_PROCESS_REQUEST, selbox)
            gen_placeholder.empty()
            report_container = st.container()
            report_container.write(
                f"""
                <div style="
                    background-color: #ffffff;
                    border: 1px solid #e0e0e0;
                    border-radius: 12px;
                    padding: 20px;
                    margin-bottom: 20px;
                    transition: transform 0.2s;
                    color: black">
                    <h3 style="text-align: center;">PROCESS REPORT</h3>
                    <p><strong>Actual Duration</strong>: {ActualDurationInfo[COL_DURATION_ACTUAL].iloc[0]}</p>
                    <p><strong>Material Used</strong>: {MaterialUsedInfo[COL_MATERIAL_NAME].iloc[0]}</p>
                    <p><strong>Material Consumed</strong>: {MaterialConsumedInfo[COL_QUANTITY_ACTUAL].iloc[0]}</p>
                    <p><strong>Feed Rate</strong>: {FeedRateInfo[COL_FEEDRATE].iloc[0]}</p>
                    <p><strong>Spindle Speed</strong>: {SpindleSpeedInfo[COL_SPINDLESPEED].iloc[0]}</p>
                    <p><strong>Depth of Cut</strong>: {DoCInfo[COL_DOC].iloc[0]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            spacer = st.empty()
            spacer.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
            if st.session_state["defectCheck"] == False:
                with stylable_container(
                    key="nodefect_container",
                    css_styles="""
                        button {
                            background-color: #4CAF50;
                            color: white;
                            padding: 14px;
                            font-size: 18px;
                            border: none;
                            border-radius: 12px;
                            width: 100%;
                            margin-top: 10px;
                            cursor: pointer;
                        }
                        button:hover {
                            background-color: #4CAF49;
                        }
                    """,
                ):
                    defect_clicked = st.button("Defect Not Found", on_click=defect_detected)
                with stylable_container(
                    key="defect_container",
                    css_styles="""
                        button {
                            background-color: #f44336;
                            color: white;
                            padding: 14px;
                            font-size: 18px;
                            border: none;
                            border-radius: 12px;
                            width: 100%;
                            margin-top: 10px;
                            cursor: pointer;
                        }
                        button:hover {
                            background-color: #d32f2f;
                        }
                    """,
                ):
                    no_defect_clicked = st.button("Defect Found", on_click=no_defect_detected)
        else:
            st.session_state["Finished"] = True
            alterstatus(TBL_PROCESS_ACTUAL, "Finish", selbox)
            st.rerun()
