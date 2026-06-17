## Import tools ____________________________________________________________________________________________________________________
import pandas as pd
from openpyxl import load_workbook
from openpyxl import Workbook
file_path = r"C:\Users\Rizky Miftah Alfiah\Downloads\PYTHON\ALGORITMA PYTHON_MODUL 4_C15_OptiCapture.xlsx"
workbook = load_workbook(file_path)
Data = workbook['Data']
import matplotlib.pyplot as plt
import time

## Mulai perhitungan waktu _________________________________________________________________________________________________________
start = time.time()

## Indeks __________________________________________________________________________________________________________________________
m = 0                               #Indeks departemen m = 1,2,...,N + R + 1
n = 0                               #Indeks departemen n = 1,2,...,N + R + 1
a = 0                               #Indeks departemen a = 1,2,...,N + R + 1
b = 0                               #Indeks departemen b = 1,2,...,N + R + 1
k = 1                               #Indeks orientasi departemen, k = 1,2,3,4
d = 0                               #Indeks arah gerak, d = 0,1,2,3

## Variabel keputusan ______________________________________________________________________________________________________________
x_in = {}                           #Koordinat titik pasok departemen pada sumbu-x
y_in = {}                           #Koordinat titik pasok departemen pada sumbu-y
x = {}                              #Koordinat titik pusat departemen pada sumbu-x
y = {}                              #Koordinat titik pusat departemen pada sumbu-y
H_bound = {}                        #Jarak horizontal batas departemen dari titik pusatnya
V_bound = {}                        #Jarak vertikal batas departemen dari titik pusatnya

## Input parameter _________________________________________________________________________________________________________________
# Data lantai produksi
F_Length = Data['D4'].value         #Panjang horizontal lantai produksi
F_Width = Data['D5'].value          #Lebar vertikal lantai produksi
N = Data['D6'].value                #Jumlah departemen
R = Data['D7'].value                #Jumlah area restriksi

# Data departemen
Length = {}                         
Width = {}
H_in = {}
V_in = {}
New = {}
Fixed = {}
Label = {}
Color = {}
Flow = {}
Cost = {}
F = 0                     
for m in range (1,N+1) :
    Length[m] = Data['D'+str(11+m)].value               #Panjang horizontal departemen m
    Width[m] = Data['E'+str(11+m)].value                #Lebar vertikal departemen m
    H_in[m] = Data['F'+str(11+m)].value                 #Jarak horizontal titik pasok departemen m dari titik pusatnya pada orientasi awal
    V_in[m] = Data['G'+str(11+m)].value                 #Jarak vertikal titik pasok departemen m dari titik pusatnya pada orientasi awal
    New[m] = Data['H'+str(11+m)].value                  #Ketetapan baru/tidaknya (eksisting) departemen m
    Fixed[m] = Data['K'+str(11+m)].value                #Ketetapan lokasi departemen m
    if (New[m] == 0) :
        F = F + 1
        x[m] = Data['I'+str(11+m)].value                #Koordinat sumbu-x departemen m
        y[m] = Data['J'+str(11+m)].value                #Koordinat sumbu-y departemen m
    Label[m] = Data['L'+str(11+m)].value                #Label departemen m
    Color[m] = Data['N'+str(11+m)].value                #Warna departemen m
for m in range (N+1,N+R+1) :
    Length[m] = Data['D'+str(15+m)].value               #Panjang horizontal area restriksi m
    Width[m] = Data['E'+str(15+m)].value                #Lebar vertikal area restriksi m
    H_in[m] = 0                                         #Jarak horizontal titik pasok area restriksi m dari titik pusatnya adalah 0
    V_in[m] = 0                                         #Jarak vertikal titik pasok area restriksi m dari titik pusatnya adalah 0
    New[m] = 0                                          #Ketetapan baru/tidaknya (eksisting) area restriksi m
    Fixed[m] = 1                                        #Ketetapan lokasi area restriksi m
    x[m] = Data['F'+str(15+m)].value                    #Koordinat titik pusat area restriksi m pada sumbu-x 
    y[m] = Data['G'+str(15+m)].value                    #Koordinat titik pusat area restriksi m pada sumbu-y
    Label[m] = Data['H'+str(15+m)].value                #Label area restriksi m
    Color[m] = Data['J'+str(15+m)].value                #Warna area restriksi m

# Data aliran material dan biaya penanganan
for m in range (1,N+R+1) :
    if (N <= 23) :
       for n in range (1,N+1) :
            f_val = Data[chr(99+n)+str(18+N+R+m)].value
            c_val = Data[chr(99+n)+str(21+2*N+R+m)].value
            Flow[(m,n)] = f_val if f_val is not None else 0                 #Jumlah aliran material dari departemen m menuju n
            Cost[(m,n)] = c_val if c_val is not None else 0                 #Biaya penanganan material dari departemen m menuju n 
    else :
        for n in range (1,24) :
            f_val = Data[chr(99+n)+str(18+N+R+m)].value
            c_val = Data[chr(99+n)+str(21+2*N+R+m)].value
            Flow[(m,n)] = f_val if f_val is not None else 0                 #Jumlah aliran material dari departemen m menuju n
            Cost[(m,n)] = c_val if c_val is not None else 0                 #Biaya penanganan material dari departemen m menuju n 
        for n in range (24,N+1) :
            f_val = Data[chr(97)+chr(97+n-24)+str(18+N+R+m)].value
            c_val = Data[chr(97)+chr(97+n-24)+str(21+2*N+R+m)].value
    if (m > N) :
        for n in range (1,N+R+1) :
            Flow[(m,n)] = 0                                                 #Jumlah aliran material dari area restriksi m menuju departemen n adalah 0
            Flow[(n,m)] = 0                                                 #Jumlah aliran material dari departemen n menuju area restriksi m adalah 0
            Cost[(m,n)] = 0                                                 #Biaya penanganan material dari area restriksi m menuju departemen n adalah 0
            Cost[(n,m)] = 0                                                 #Biaya penanganan material dari departemen n menuju area restriksi m adalah 0

## Inisiasi _______________________________________________________________________________________________________________________
Allocate_First = []                                 #Urutan departemen yang dialokasikan terlebih dahulu
Allocate_Next = []                                  #Urutan departemen yang dialokasikan setelahnya
Sequence = {}                           
for m in range (1,N+R+1) :
    if (New[m] != 1) :                
        x_in[m] = x[m] + H_in[m]                    #Perhitungan koordinat titik input departemen eksisting m pada sumbu-x
        y_in[m] = y[m] + V_in[m]                    #Perhitungan koordinat titik input departemen eksisting m pada sumbu-y
        H_bound[m] = Length[m]/2                    #Jarak horizontal batas departemen eksisting m dari titik pusatnya adalah setengah dari panjang departemen
        V_bound[m] = Width[m]/2                     #Jarak vertikal batas departemen eksisting m dari titik pusatnya adalah setengah dari lebar departemen
        Allocate_First.append(m)                    #Departemen dan area restriksi eksisting akan dialokasikan terlebih dahulu
    else :
        Sequence[m] = Data['O'+str(11+m)].value     #Urutan alokasi departemen baru m

Sorted_Sequence = dict(sorted(Sequence.items(), key = lambda item: item[1]))
for m in (Sorted_Sequence.keys()) :
    Allocate_Next.append(m)                         #Departemen baru akan dialokasikan setelahnya

if (len(Allocate_First) == 0) :
    m = Allocate_Next[0]                            #Jika tidak ada departemen atau area restriksi eksisting, departemen yang dialokasikan pertama adalah departemen baru
    Allocate_First.append(m)                        #Departemen m ditambahkan di alokasi pertama
    Allocate_Next.remove(m)                         #Departemen m dihapus dari alokasi setelahnya
    New[m] = 0                        
    x[m] = F_Length/2                               #Koodinat-x departemen m diposisikan di tengah lantai produksi
    y[m] = F_Width/2                                #Koodinat-y departemen m diposisikan di tengah lantai produksi
    x_in[m] = x[m] + H_in[m]                        #Perhitungan koordinat titik input departemen baru m pada sumbu-x
    y_in[m] = y[m] + V_in[m]                        #Perhitungan koordinat titik input departemen baru m pada sumbu-y
    H_bound[m] = Length[m]/2                        #Jarak horizontal batas departemen baru m dari titik pusatnya adalah setengah dari panjang departemen
    V_bound[m] = Width[m]/2                         #Jarak vertikal batas departemen baru m dari titik pusatnya adalah setengah dari lebar departemen
 
## Urutan penempatan departemen ____________________________________________________________________________________________________
To_Be_Allocated = Allocate_First + Allocate_Next    #Urutan alokasi departemen keseluruhan

## Zona penempatan awal ____________________________________________________________________________________________________________
p = 0                                               #Indeks kumpulan zona ke-p
Zone_start_x = {(p,1):0}                            #Batas kiri zona awal adalah 0
Zone_start_y = {(p,1):0}                            #Batas bawah zona awal adalah 0
Zone_end_x = {(p,1):F_Length}                       #Batas kanan zona awal adalah panjang horizontal lantai produksi
Zone_end_y = {(p,1):F_Width}                        #Batas atas zona awal adalah lebar vertikal lantai produksi
q = 1                                               #Jumlah zona penempatan tersedia saat ini = 1
PMHC_opt = 0                                        #Partial Material Handling Cost (PMHC) optimal awal = 0

## Algoritma konstruksi ____________________________________________________________________________________________________________
Allocated = []                                      
Unallocateable = []
Stop_Allocation = False
before = 0

while (Stop_Allocation == False) :
    for m in To_Be_Allocated :
        if (New[m] == 1) :                           

        ## Median Method (3M)

            #Inisiasi
            MM_x_in = list(set(x_in.values()))            
            MM_y_in = list(set(y_in.values()))             
            sum_weight_x_in = 0
            sum_weight_y_in = 0
            order_x_in = {}
            order_y_in = {}
            stop = False

            #Perhitungan bobot total
            i = 0
            j = 0
            while (stop == False) :
                for n in Allocated :
                    if (len(MM_x_in) != 0) :
                        if (x_in[n] == min(MM_x_in)) :
                            sum_weight_x_in = sum_weight_x_in + Cost[(m,n)]*Flow[(m,n)] + Cost[(n,m)]*Flow[(n,m)]
                            i = i + 1
                            order_x_in[i] = n
                    if (len(MM_y_in) != 0) :
                        if (y_in[n] == min(MM_y_in)) :
                            sum_weight_y_in = sum_weight_y_in + Cost[(m,n)]*Flow[(m,n)] + Cost[(n,m)]*Flow[(n,m)]
                            j = j + 1
                            order_y_in[j] = n
                if (len(MM_x_in) != 0) :
                    MM_x_in.remove(min(MM_x_in))
                if (len(MM_y_in) != 0) :
                    MM_y_in.remove(min(MM_y_in))
                if (len(MM_x_in) == 0) and (len(MM_y_in) == 0) :
                    stop = True
            
            #Pencarian median
            half_weight_x_in = sum_weight_x_in/2
            half_weight_y_in = sum_weight_y_in/2
            sum_weight_x_in = 0
            sum_weight_y_in = 0
            a = 1
            b = 1
            while (a < i+1) :
                sum_weight_x_in = sum_weight_x_in + Cost[(m,order_x_in[a])]*Flow[(m,order_x_in[a])] + Cost[(order_x_in[a],m)]*Flow[(order_x_in[a],m)]
                if (sum_weight_x_in >= half_weight_x_in) :
                    x_in[m] = x_in[order_x_in[a]]
                    a = i + 1
                else :
                    a = a + 1  
            while (b < j+1) :
                sum_weight_y_in = sum_weight_y_in + Cost[(m,order_y_in[b])]*Flow[(m,order_y_in[b])] + Cost[(order_y_in[b],m)]*Flow[(order_y_in[b],m)]
                if (sum_weight_y_in >= half_weight_y_in) :
                    y_in[m] = y_in[order_y_in[b]]
                    b = j + 1
                else :
                    b = b + 1 
            Allocated.append(m)

            #Pergeseran titik median
            PMHC_opt = float('inf')
            n_x_in = x_in[m]
            n_y_in = y_in[m]
            count = 0
            for k in range (1,5) :
                if (k == 1) :
                    n_H_bound = Length[m]/2
                    n_V_bound = Width[m]/2
                    n_x = n_x_in + H_in[m]
                    n_y = n_y_in + V_in[m]
                if (k == 2) :
                    n_H_bound = Width[m]/2
                    n_V_bound = Length[m]/2
                    n_x = n_x_in + V_in[m]
                    n_y = n_y_in + H_in[m]
                if (k == 3) :
                    n_H_bound = Length[m]/2
                    n_V_bound = Width[m]/2
                    n_x = n_x_in - H_in[m]
                    n_y = n_y_in - V_in[m]
                if (k == 4) :
                    n_H_bound = Width[m]/2
                    n_V_bound = Length[m]/2
                    n_x = n_x_in - V_in[m]
                    n_y = n_y_in - H_in[m]
                for i in range(1,q+1) :
                    n_x_in_q = n_x_in
                    n_y_in_q = n_y_in
                    n_x_q = n_x
                    n_y_q = n_y
                    if (2*n_H_bound <= Zone_end_x[(p,i)]-Zone_start_x[(p,i)]) and (2*n_V_bound <= Zone_end_y[(p,i)]-Zone_start_y[(p,i)]):
                        if (n_x-n_H_bound < Zone_start_x[(p,i)]) :
                            move_dist = Zone_start_x[(p,i)] - (n_x - n_H_bound)
                            n_x_q = n_x + move_dist
                            n_x_in_q = n_x_in + move_dist
                            x_in[m] = n_x_in_q
                        if (n_x+n_H_bound > Zone_end_x[(p,i)]) :
                            move_dist = Zone_end_x[(p,i)] - (n_x + n_H_bound)
                            n_x_q = n_x + move_dist
                            n_x_in_q = n_x_in + move_dist
                            x_in[m] = n_x_in_q
                        if (n_y-n_V_bound < Zone_start_y[(p,i)]) :
                            move_dist = Zone_start_y[(p,i)] - (n_y - n_V_bound)
                            n_y_q = n_y + move_dist
                            n_y_in_q = n_y_in_q + move_dist
                            y_in[m] = n_y_in_q
                        if (n_y+n_V_bound > Zone_end_y[(p,i)]) :
                            move_dist = Zone_end_y[(p,i)] - (n_y + n_V_bound)
                            n_y_q = n_y + move_dist
                            n_y_in_q = n_y_in_q + move_dist
                            y_in[m] = n_y_in_q
                        
                        #Perhitungan PMHC
                        PMHC = 0
                        for a in Allocated :
                            for b in Allocated :
                                PMHC = PMHC + Cost[(a,b)]*Flow[(a,b)]*(abs(x_in[a] - x_in[b]) + abs(y_in[a] - y_in[b]))
                        
                        if (PMHC < PMHC_opt) :
                            PMHC_opt = PMHC
                            x_in_opt = n_x_in_q
                            y_in_opt = n_y_in_q
                            x_opt = n_x_q
                            y_opt = n_y_q
                            H_bound_opt = n_H_bound
                            V_bound_opt = n_V_bound        
                        x_in[m] = n_x_in
                        y_in[m] = n_y_in

                    else :
                        count = count + 1

            #Input variabel keputusan
            if (count == 4*q) :
                Unallocateable.append(m)
                Allocated.remove(m)
                del x_in[m]
                del y_in[m]
            else :
                x_in[m] = x_in_opt
                y_in[m] = y_in_opt
                x[m] = x_opt
                y[m] = y_opt
                H_bound[m] = H_bound_opt
                V_bound[m] = V_bound_opt

        else:
            Allocated.append(m)

        if m in Allocated:

        ## Zone Algorithm (ZA)

            #Inisiasi
            p = p + 1
            overlap = {}
            Zone_start_x_s = {}
            Zone_start_y_s = {}
            Zone_end_x_s = {}
            Zone_end_y_s = {}

            for s in range (1,q+1) :

                if (y[m]+V_bound[m] > Zone_start_y[(p-1,s)]) and (y[m]-V_bound[m] < Zone_end_y[(p-1,s)]) and (x[m]+H_bound[m] > Zone_start_x[(p-1,s)]) and (x[m]-H_bound[m] < Zone_end_x[(p-1,s)]) :
                    overlap[s] = True

                    # Membuat dummy
                    for t in range (1,5) :
                        Zone_start_x_s[(s,t)] = 0
                        Zone_start_y_s[(s,t)] = 0
                        Zone_end_x_s[(s,t)] = 0
                        Zone_end_y_s[(s,t)] = 0
                    
                    if (Zone_start_x[(p-1,s)] <= x[m]-H_bound[m]):
                        Zone_start_x_s[(s,1)] = Zone_start_x[(p-1,s)]
                        Zone_start_y_s[(s,1)] = Zone_start_y[(p-1,s)]
                        Zone_end_x_s[(s,1)] = x[m] - H_bound[m]
                        Zone_end_y_s[(s,1)] = Zone_end_y[(p-1,s)]
                    if (Zone_end_y[(p-1,s)] >= y[m]+V_bound[m]):
                        Zone_start_x_s[(s,2)] = Zone_start_x[(p-1,s)]
                        Zone_start_y_s[(s,2)] = y[m] + V_bound[m]
                        Zone_end_x_s[(s,2)] = Zone_end_x[(p-1,s)]
                        Zone_end_y_s[(s,2)] = Zone_end_y[(p-1,s)]
                    if (Zone_end_x[(p-1,s)] >= x[m]+H_bound[m]):
                        Zone_start_x_s[(s,3)] = x[m] + H_bound[m]
                        Zone_start_y_s[(s,3)] = Zone_start_y[(p-1,s)]
                        Zone_end_x_s[(s,3)] = Zone_end_x[(p-1,s)]
                        Zone_end_y_s[(s,3)] = Zone_end_y[(p-1,s)]
                    if (Zone_start_y[(p-1,s)] <= y[m]-V_bound[m]):
                        Zone_start_x_s[(s,4)] = Zone_start_x[(p-1,s)]
                        Zone_start_y_s[(s,4)] = Zone_start_y[(p-1,s)]
                        Zone_end_x_s[(s,4)] = Zone_end_x[(p-1,s)]
                        Zone_end_y_s[(s,4)] = y[m] - V_bound[m]
                    
                else :
                    overlap[s] = False

            #Memisahkan dummy 
            count = 0
            Zone_start_x_group = {}
            Zone_start_y_group = {}
            Zone_end_x_group = {}
            Zone_end_y_group = {}
            for s in range (1,q+1) :
                if (overlap[s] == True) :
                    for t in range (1,5) :
                        if (Zone_end_x_s[(s,t)] - Zone_start_x_s[(s,t)] > 1e-14) and (Zone_end_y_s[(s,t)] - Zone_start_y_s[(s,t)] > 1e-14) :
                            count = count + 1
                            Zone_start_x_group[count] = Zone_start_x_s[(s,t)]
                            Zone_start_y_group[count] = Zone_start_y_s[(s,t)]
                            Zone_end_x_group[count] = Zone_end_x_s[(s,t)]
                            Zone_end_y_group[count] = Zone_end_y_s[(s,t)]
                else :
                    count = count + 1
                    Zone_start_x_group[count] = Zone_start_x[(p-1,s)]
                    Zone_start_y_group[count] = Zone_start_y[(p-1,s)]
                    Zone_end_x_group[count] = Zone_end_x[(p-1,s)]
                    Zone_end_y_group[count] = Zone_end_y[(p-1,s)]

            #Menghapus zona duplikat atau contained
            delete = []
            for a in range (1,count+1) :
                for b in range (1,count+1) :
                    if (a != b) :
                        if (Zone_start_x_group[a] >= Zone_start_x_group[b]) and (Zone_start_y_group[a] >= Zone_start_y_group[b]) and (Zone_end_x_group[a] <= Zone_end_x_group[b]) and (Zone_end_y_group[a] <= Zone_end_y_group[b]) :
                            delete.append(a)
            unique_delete = list(set(delete))
            for a in unique_delete :
                del Zone_start_x_group[a]
                del Zone_start_y_group[a]
                del Zone_end_x_group[a]
                del Zone_end_y_group[a]
            
            #Membuat zona baru
            Assigned_x_start = list(Zone_start_x_group.values())
            count = 0
            for a in Assigned_x_start :
                count = count + 1
                Zone_start_x[(p,count)] = a
            Assigned_y_start = list(Zone_start_y_group.values())
            count = 0
            for a in Assigned_y_start :
                count = count + 1
                Zone_start_y[(p,count)] = a 
            Assigned_x_end = list(Zone_end_x_group.values())
            count = 0 
            for a in Assigned_x_end :
                count = count + 1 
                Zone_end_x[(p,count)] = a
            Assigned_y_end = list(Zone_end_y_group.values())
            count = 0
            for a in Assigned_y_end :
                count = count + 1
                Zone_end_y[(p,count)] = a
            q = count 
        
        #Perhitungan PMHC
        PMHC = 0
        for a in Allocated :
            for b in Allocated :
                PMHC = PMHC + Cost[(a,b)]*Flow[(a,b)]*(abs(x_in[a] - x_in[b]) + abs(y_in[a] - y_in[b]))      
        
        #Visualisasi 
        Time = '-'
        plt.figure(figsize=(8,8))
        fig = plt.gcf()
        ax = fig.gca()
        Rect = {}
        Point = {}
        Text = {}
        Zone = {}
        F_Rect = plt.Rectangle(xy=(0,0), width=F_Length, height=F_Width, color='w')
        ax.add_patch(F_Rect)
        for a in Allocated :
            Rect[a] = plt.Rectangle(xy=(x[a]-H_bound[a],y[a]-V_bound[a]), fill=True, width=2*H_bound[a], height=2*V_bound[a], edgecolor = 'black', fc=Color[a])
            ax.add_patch(Rect[a])
            Text[a] = plt.text(x[a]-V_bound[a]/5,y[a]-2*V_bound[a]/3,Label[a])
        for a in range(1,q+1) :
            Zone[a] = plt.Rectangle(xy=(Zone_start_x[(p,a)],Zone_start_y[(p,a)]), fill=False, width=Zone_end_x[(p,a)]-Zone_start_x[(p,a)], height=Zone_end_y[(p,a)]-Zone_start_y[(p,a)], edgecolor = 'r')
            ax.add_patch(Zone[a])
        for a in Allocated :
            if (a < N+1) :
                Point[a] = plt.Rectangle(xy=(x_in[a],y_in[a]), fill=True, width=F_Width/150, height=F_Width/150, color='black')
                ax.add_patch(Point[a])
        plt.text(0,F_Width + 1,'PMHC = ' + str(PMHC))
        plt.text(0,F_Width + 1 + F_Width/40,'Time = ' + str(Time))
        plt.text(F_Length/2,F_Width + 1,'Unallocatable = ' + str(len(Unallocateable)))
        plt.text(F_Length/2,F_Width + 1 + F_Width/40,'Allocated = ' + str(len(Allocated)))
        plt.xlim([0,F_Length])
        plt.ylim([0,F_Width])
        plt.show()

    ## Algoritma perbaikan ____________________________________________________________________________________________________________

    #Membuat dummy batas lantai produksi
    x[N+R+1] = 0
    y[N+R+1] = F_Width/2
    H_bound[N+R+1] = 0
    V_bound[N+R+1] = F_Width/2
    x[N+R+2] = F_Length
    y[N+R+2] = F_Width/2
    H_bound[N+R+2] = 0
    V_bound[N+R+2] = F_Width/2
    x[N+R+3] = F_Length/2
    y[N+R+3] = 0
    H_bound[N+R+3] = F_Length/2
    V_bound[N+R+3] = 0
    x[N+R+4] = F_Length/2
    y[N+R+4] = F_Width
    H_bound[N+R+4] = F_Length/2
    V_bound[N+R+4] = 0
    for m in range (N+R+1,N+R+5) :
        x_in[m] = x[m]
        y_in[m] = y[m]
        Fixed[m] = 1
        for n in range (1,N+R+5) :
            Flow[(n,m)] = 0
            Flow[(m,n)] = 0
            Cost[(n,m)] = 0
            Cost[(m,n)] = 0
        Allocated.append(m)
        Color[m] = 'b'
        Label[m] = 'H'

    optimal = False
    while (optimal == False) :
        stop = False
        while (stop == False) :

        ## Group Movement (GM)

            #Pembuatan group horizontal
            To_be_group = list(Allocated)
            H_group = {1:[]}
            for n in To_be_group :
                if (Fixed[n] != 1) :
                    H_group[1] = H_group[1] + [n]
                    To_be_group.remove(n)
                    break
            for n in To_be_group :
                if (Fixed[n] != 1) :
                    t = 1
                    m = False
                    while (t < max(H_group.keys())+1) :
                        for a in H_group[t] :
                            if ((x[n]+H_bound[n] == x[a]-H_bound[a]) or (x[n]-H_bound[n] == x[a]+H_bound[a])) and (y[a]+V_bound[a] > y[n]-V_bound[n]) and (y[a]-V_bound[a] < y[n]+V_bound[n]) :
                                if (m == False) :
                                    m = t
                                    H_group[t] = H_group[t] + [n]
                                elif (m != False) :
                                    H_group[m] = H_group[m] + H_group[t]
                                    del H_group[t]
                                    n_H_group = []
                                    for b in H_group.keys() :
                                        n_H_group.append(b)
                                    for b in n_H_group :
                                        if (b > t) :
                                            H_group[b-1] = H_group[b]
                                            del H_group[b]
                                    t = t - 1
                                break
                        t = t + 1
                    if (m == False) :
                        H_group[max(H_group.keys())+1] = [n]
            
            #Pembuatan group vertikal
            To_be_group = list(Allocated)
            V_group = {1:[]}
            for n in To_be_group :
                if (Fixed[n] != 1) :
                    V_group[1] = V_group[1] + [n]
                    To_be_group.remove(n)
                    break
            for n in To_be_group :
                if (Fixed[n] != 1) :
                    t = 1
                    m = False
                    while (t < max(V_group.keys())+1) :
                        for a in V_group[t] :
                            if ((y[n]+V_bound[n] == y[a]-V_bound[a]) or (y[n]-V_bound[n] == y[a]+V_bound[a])) and (x[a]+H_bound[a] > x[n]-H_bound[n]) and (x[a]-H_bound[a] < x[n]+H_bound[n]) :
                                if (m == False) :
                                    m = t
                                    V_group[t] = V_group[t] + [n]
                                elif (m != False) :
                                    V_group[m] = V_group[m] + V_group[t]
                                    del V_group[t]
                                    n_V_group = []
                                    for b in V_group.keys() :
                                        n_V_group.append(b)
                                    for b in n_V_group :
                                        if (b > t) :
                                            V_group[b-1] = V_group[b]
                                            del V_group[b]
                                    t = t - 1
                                break
                        t = t + 1
                    if (m == False) :
                        V_group[max(V_group.keys())+1] = [n]
            
            #Perhitungan difference
            Diff_H_in = {}
            Diff_H_out = {}
            Diff_V_in = {}
            Diff_V_out = {}
            Diff_H_group = {}
            Diff_V_group = {}
            group_move_dist = {}
            RDC_opt = 0
            for k in range (0,4) :
                if (k == 0) or (k == 2) :
                    for m in (H_group.keys()) :
                        Diff_H_group[(m,k)] = 0
                        group_move_dist[(m,k)] = float('inf')
                        for n in H_group[m] :
                            Diff_H_in[(n,k)] = 0
                            Diff_H_out[(n,k)] = 0
                            if (k == 0) :
                                for a in Allocated :
                                    if a not in H_group[m] :
                                        if (x_in[a] < x_in[n]) :
                                            Diff_H_in[(n,k)] = Diff_H_in[(n,k)] - Cost[(a,n)]*Flow[(a,n)]
                                            Diff_H_out[(n,k)] = Diff_H_out[(n,k)] - Cost[(n,a)]*Flow[(n,a)]
                                            group_move_dist[(m,k)] = min(group_move_dist[(m,k)],x_in[n]-x_in[a])
                                        if (x_in[a] >= x_in[n]) :
                                            Diff_H_in[(n,k)] = Diff_H_in[(n,k)] + Cost[(a,n)]*Flow[(a,n)]
                                            Diff_H_out[(n,k)] = Diff_H_out[(n,k)] + Cost[(n,a)]*Flow[(n,a)]
                                        if (x[a]+H_bound[a] <= x[n]+H_bound[n]) and (y[a]-V_bound[a] < y[n]+V_bound[n]) and (y[a]+V_bound[a] > y[n]-V_bound[n]) :
                                            group_move_dist[(m,k)] = min(group_move_dist[(m,k)],x[n]-H_bound[n] - (x[a]+H_bound[a]))
                            if (k == 2) :
                                for a in Allocated :
                                    if a not in H_group[m] :
                                        if (x_in[a] <= x_in[n]) :
                                            Diff_H_in[(n,k)] = Diff_H_in[(n,k)] + Cost[(a,n)]*Flow[(a,n)]
                                            Diff_H_out[(n,k)] = Diff_H_out[(n,k)] + Cost[(n,a)]*Flow[(n,a)]
                                        if (x_in[a] > x_in[n]) :
                                            Diff_H_in[(n,k)] = Diff_H_in[(n,k)] - Cost[(a,n)]*Flow[(a,n)]
                                            Diff_H_out[(n,k)] = Diff_H_out[(n,k)] - Cost[(n,a)]*Flow[(n,a)]
                                            group_move_dist[(m,k)] = min(group_move_dist[(m,k)],x_in[a]-x_in[n])
                                        if (x[a]-H_bound[a] >= x[n]-H_bound[n]) and (y[a]-V_bound[a] < y[n]+V_bound[n]) and (y[a]+V_bound[a] > y[n]-V_bound[n]) :
                                            group_move_dist[(m,k)] = min(group_move_dist[(m,k)],x[a]-H_bound[a] - (x[n]+H_bound[n]))
                            Diff_H_group[(m,k)] = Diff_H_group[(m,k)] + Diff_H_in[(n,k)] + Diff_H_out[(n,k)]
                        if (Diff_H_group[(m,k)] < 0) :
                            RDC = Diff_H_group[(m,k)] * group_move_dist[(m,k)]
                            if (RDC < RDC_opt) :
                                RDC_opt = RDC
                                m_opt = m
                                k_opt = k
                                group_move_dist_opt = group_move_dist[(m,k)]
                if (k == 1) or (k == 3) :
                    for m in (V_group.keys()) :
                        Diff_V_group[(m,k)] = 0
                        group_move_dist[(m,k)] = float('inf')
                        for n in V_group[m] :
                            Diff_V_in[(n,k)] = 0
                            Diff_V_out[(n,k)] = 0
                            if (k == 3) :
                                for a in Allocated :
                                    if a not in V_group[m] :
                                        if (y_in[a] < y_in[n]) :
                                            Diff_V_in[(n,k)] = Diff_V_in[(n,k)] - Cost[(a,n)]*Flow[(a,n)]
                                            Diff_V_out[(n,k)] = Diff_V_out[(n,k)] - Cost[(n,a)]*Flow[(n,a)]
                                            group_move_dist[(m,k)] = min(group_move_dist[(m,k)],y_in[n]-y_in[a])
                                        if (y_in[a] >= y_in[n]) :
                                            Diff_V_in[(n,k)] = Diff_V_in[(n,k)] + Cost[(a,n)]*Flow[(a,n)]
                                            Diff_V_out[(n,k)] = Diff_V_out[(n,k)] + Cost[(n,a)]*Flow[(n,a)]
                                        if (y[a]+V_bound[a] <= y[n]+V_bound[n]) and (x[a]-H_bound[a] < x[n]+H_bound[n]) and (x[a]+H_bound[a] > x[n]-H_bound[n]) :
                                            group_move_dist[(m,k)] = min(group_move_dist[(m,k)],y[n]-V_bound[n] - (y[a]+V_bound[a]))
                            if (k == 1) :
                                for a in Allocated :
                                    if a not in V_group[m] :
                                        if (y_in[a] <= y_in[n]) :
                                            Diff_V_in[(n,k)] = Diff_V_in[(n,k)] + Cost[(a,n)]*Flow[(a,n)]
                                            Diff_V_out[(n,k)] = Diff_V_out[(n,k)] + Cost[(n,a)]*Flow[(n,a)]
                                        if (y_in[a] > y_in[n]) :
                                            Diff_V_in[(n,k)] = Diff_V_in[(n,k)] - Cost[(a,n)]*Flow[(a,n)]
                                            Diff_V_out[(n,k)] = Diff_V_out[(n,k)] - Cost[(n,a)]*Flow[(n,a)]
                                            group_move_dist[(m,k)] = min(group_move_dist[(m,k)],y_in[a]-y_in[n])
                                        if (y[a]-V_bound[a] >= y[n]-V_bound[n]) and (x[a]-H_bound[a] < x[n]+H_bound[n]) and (x[a]+H_bound[a] > x[n]-H_bound[n]) :
                                            group_move_dist[(m,k)] = min(group_move_dist[(m,k)],y[a]-V_bound[a] - (y[n]+V_bound[n]))
                            Diff_V_group[(m,k)] = Diff_V_group[(m,k)] + Diff_V_in[(n,k)] + Diff_V_out[(n,k)]
                        if (Diff_V_group[(m,k)] < 0) :
                            RDC = Diff_V_group[(m,k)] * group_move_dist[(m,k)]
                            if (RDC < RDC_opt) :
                                RDC_opt = RDC
                                m_opt = m
                                k_opt = k
                                group_move_dist_opt = group_move_dist[(m,k)]
            
            #Penentuan pergeseran
            if (RDC_opt < 0) :
                if (k_opt == 0) :
                    for n in H_group[m_opt] :
                        n_x = x[n]
                        x[n] = x[n] - group_move_dist_opt
                        x_in[n] = x_in[n] - group_move_dist_opt
                        if (n_x == x[n]) :
                            stop = True
                if (k_opt == 1) :
                    for n in V_group[m_opt] :
                        n_y = y[n]
                        y[n] = y[n] + group_move_dist_opt
                        y_in[n] = y_in[n] + group_move_dist_opt
                        if (n_y == y[n]) :
                            stop = True
                if (k_opt == 2) :
                    for n in H_group[m_opt] :
                        n_x = x[n]
                        x[n] = x[n] + group_move_dist_opt
                        x_in[n] = x_in[n] + group_move_dist_opt
                        if (n_x == x[n]) :
                            stop = True
                if (k_opt == 3) :
                    for n in V_group[m_opt] :
                        n_y = y[n]
                        y[n] = y[n] - group_move_dist_opt
                        y_in[n] = y_in[n] - group_move_dist_opt
                        if (n_y == y[n]) :
                            stop = True
                
            else :
                stop = True
                
                #Perhitungan TMHC
                TMHC = 0
                for a in Allocated :
                    for b in Allocated :
                        TMHC = TMHC + Cost[(a,b)]*Flow[(a,b)]*(abs(x_in[a] - x_in[b]) + abs(y_in[a] - y_in[b]))     
                
                #Visualisasi
                Time = '-'
                plt.figure(figsize=(8,8))
                fig = plt.gcf()
                ax = fig.gca()
                Rect = {}
                Point = {}
                Text = {}
                F_Rect = plt.Rectangle(xy=(0,0), width=F_Length, height=F_Width, color='w')
                ax.add_patch(F_Rect)
                for a in Allocated :
                    Rect[a] = plt.Rectangle(xy=(x[a]-H_bound[a],y[a]-V_bound[a]), fill=True, width=2*H_bound[a], height=2*V_bound[a], edgecolor = 'black', fc=Color[a])
                    ax.add_patch(Rect[a])
                    if (a < 9) :
                        Text[a] = plt.text(x[a]-V_bound[a]/5,y[a]-2*V_bound[a]/3,Label[a])
                for a in Allocated :
                    if (a < N+1) :
                        Point[a] = plt.Rectangle(xy=(x_in[a],y_in[a]), fill=True, width=F_Width/150, height=F_Width/150, color='black')
                        ax.add_patch(Point[a])
                plt.text(0,F_Width + 1,'TMHC = ' + str(TMHC))
                plt.text(0,F_Width + 1 + F_Width/40,'Time = ' + str(Time))
                plt.text(F_Length/2,F_Width + 1,'Unallocatable = ' + str(len(Unallocateable)))
                plt.text(F_Length/2,F_Width + 1 + F_Width/40,'Allocated = ' + str(len(Allocated)))
                plt.xlim([0,F_Length])
                plt.ylim([0,F_Width])
                plt.show()
                
            print (stop)
        
        #Perhitungan Total Material Handling Cost (TMHC)
        TMHC_opt = 0
        for a in Allocated :
            for b in Allocated :
                TMHC_opt = TMHC_opt + Cost[(a,b)]*Flow[(a,b)]*(abs(x_in[a] - x_in[b]) + abs(y_in[a] - y_in[b]))  

        ## 2-Opt

        #Inisiasi
        TMHC_now = TMHC_opt
        for m in range (1,N+1) :
            if m in Allocated and (Fixed[m] != 1) :
                for n in range (1,N+1) :
                    if n in Allocated and (Fixed[n] != 1) and (m != n):
                        m_x = x[m]
                        m_y = y[m]
                        m_x_in = x_in[m]
                        m_y_in = y_in[m]
                        m_H_bound = H_bound[m]
                        m_V_bound = V_bound[m]
                        n_x = x[n]
                        n_y = y[n]
                        n_x_in = x_in[n]
                        n_y_in = y_in[n]
                        n_H_bound = H_bound[n]
                        n_V_bound = V_bound[n]

                        #Penentuan orientasi departemen m dan n
                        for k_m in range (1,5) :
                            for k_n in range (1,5) :

                                #Menukar posisi m dengan n
                                x[m] = n_x
                                y[m] = n_y
                                x[n] = m_x
                                y[n] = m_y
                                
                                if (k_m == 1) :
                                    H_bound[m] = Length[m]/2
                                    V_bound[m] = Width[m]/2
                                    x_in[m] = x[m] + H_in[m]
                                    y_in[m] = y[m] + V_in[m]
                                if (k_m == 2) :
                                    H_bound[m] = Width[m]/2
                                    V_bound[m] = Length[m]/2
                                    x_in[m] = x[m] + V_in[m]
                                    y_in[m] = y[m] + H_in[m]
                                if (k_m == 3) :
                                    H_bound[m] = Length[m]/2
                                    V_bound[m] = Width[m]/2
                                    x_in[m] = x[m] - H_in[m]
                                    y_in[m] = y[m] - V_in[m]
                                if (k_m == 4) :
                                    H_bound[m] = Width[m]/2
                                    V_bound[m] = Length[m]/2
                                    x_in[m] = x[m] - V_in[m]
                                    y_in[m] = y[m] - H_in[m]
                                if (k_n == 1) :
                                    H_bound[n] = Length[n]/2
                                    V_bound[n] = Width[n]/2
                                    x_in[n] = x[n] + H_in[n]
                                    y_in[n] = y[n] + V_in[n]
                                if (k_n == 2) :
                                    H_bound[n] = Width[n]/2
                                    V_bound[n] = Length[n]/2
                                    x_in[n] = x[n] + V_in[n]
                                    y_in[n] = y[n] + H_in[n]
                                if (k_n == 3) :
                                    H_bound[n] = Length[n]/2
                                    V_bound[n] = Width[n]/2
                                    x_in[n] = x[n] - H_in[n]
                                    y_in[n] = y[n] - V_in[n]
                                if (k_n == 4) :
                                    H_bound[n] = Width[n]/2
                                    V_bound[n] = Length[n]/2
                                    x_in[n] = x[n] - V_in[n]
                                    y_in[n] = y[n] - H_in[n]
                                
                                Overlap = False
                                for a in Allocated :
                                    if (y[a]-V_bound[a] < y[n]+V_bound[n]) and (y[a]-V_bound[a] > m_y+m_V_bound) and (x[a]-H_bound[a] < x[n]+H_bound[n]) and (x[a]+H_bound[a] > x[n]-H_bound[n]) and (n != a) and ((H_bound[n] != m_H_bound) or (V_bound[n] != m_V_bound)):
                                        move_dist = y[n]+V_bound[n] - (y[a]-V_bound[a])
                                        y[n] =  y[n] - move_dist
                                        y_in[n] = y_in[n] - move_dist
                                    if (y[a]-V_bound[a] < y[m]+V_bound[m]) and (y[a]-V_bound[a] > n_y+n_V_bound) and (x[a]-H_bound[a] < x[m]+H_bound[m]) and (x[a]+H_bound[a] > x[m]-H_bound[m]) and (m != a) and ((H_bound[m] != n_H_bound) or (V_bound[m] != n_V_bound)):
                                        move_dist = y[m]+V_bound[m] - (y[a]-V_bound[a])
                                        y[m] =  y[m] - move_dist
                                        y_in[m] = y_in[m] - move_dist
                                for a in Allocated :
                                    if (y[a]+V_bound[a] > y[n]-V_bound[n]) and (y[a]+V_bound[a] < m_y+m_V_bound) and (x[a]-H_bound[a] < x[n]+H_bound[n]) and (x[a]+H_bound[a] > x[n]-H_bound[n]) and (n != a) and ((H_bound[n] != m_H_bound) or (V_bound[n] != m_V_bound)):
                                        move_dist = y[a]+V_bound[a] - (y[n]-V_bound[n])
                                        y[n] =  y[n] + move_dist
                                        y_in[n] = y_in[n] + move_dist
                                    if (y[a]+V_bound[a] > y[m]-V_bound[m]) and (y[a]+V_bound[a] < n_y+n_V_bound) and (x[a]-H_bound[a] < x[m]+H_bound[m]) and (x[a]+H_bound[a] > x[m]-H_bound[m]) and (m != a) and ((H_bound[m] != n_H_bound) or (V_bound[m] != n_V_bound)):
                                        move_dist = y[a]+V_bound[a] - (y[m]-V_bound[m])
                                        y[m] =  y[m] + move_dist
                                        y_in[m] = y_in[m] + move_dist
                                for a in Allocated :
                                    if (x[a]-H_bound[a] < x[n]+H_bound[n]) and (x[a]-H_bound[a] > m_x+m_H_bound) and (y[a]-V_bound[a] < y[n]+V_bound[n]) and (y[a]+V_bound[a] > y[n]-V_bound[n]) and (n != a) and ((H_bound[n] != m_H_bound) or (V_bound[n] != m_V_bound)):
                                        move_dist = x[n]+H_bound[n] - (x[a]-H_bound[a])
                                        x[n] =  x[n] - move_dist
                                        x_in[n] = x_in[n] - move_dist
                                    if (x[a]-H_bound[a] < x[m]+H_bound[m]) and (x[a]-H_bound[a] > n_x+n_H_bound) and (y[a]-V_bound[a] < y[m]+V_bound[m]) and (y[a]+V_bound[a] > y[m]-V_bound[m]) and (m != a) and ((H_bound[m] != n_H_bound) or (V_bound[m] != n_V_bound)):
                                        move_dist = x[m]+H_bound[m] - (x[a]-H_bound[a])
                                        x[m] =  x[m] - move_dist
                                        x_in[m] = x_in[m] - move_dist
                                for a in Allocated :
                                    if (x[a]+H_bound[a] > x[n]-H_bound[n]) and (x[a]+H_bound[a] < m_x-m_H_bound) and (y[a]-V_bound[a] < y[n]+V_bound[n]) and (y[a]+V_bound[a] > y[n]-V_bound[n]) and (n != a) and ((H_bound[n] != m_H_bound) or (V_bound[n] != m_V_bound)):
                                        move_dist = x[a]+H_bound[a] - (x[n]-H_bound[n])
                                        x[n] =  x[n] + move_dist
                                        x_in[n] = x_in[n] + move_dist
                                    if (x[a]+H_bound[a] > x[m]-H_bound[m]) and (x[a]+H_bound[a] < n_x-n_H_bound) and (y[a]-V_bound[a] < y[m]+V_bound[m]) and (y[a]+V_bound[a] > y[m]-V_bound[m]) and (m != a) and ((H_bound[m] != n_H_bound) or (V_bound[m] != n_V_bound)):
                                        move_dist = x[a]+H_bound[a] - (x[m]-H_bound[m])
                                        x[m] =  x[m] + move_dist
                                        x_in[m] = x_in[m] + move_dist
                                for a in Allocated :
                                    if (y[a]-V_bound[a] < y[n]+V_bound[n]) and (y[a]+V_bound[a] > y[n]-V_bound[n]) and (x[a]-H_bound[a] < x[n]+H_bound[n]) and (x[a]+H_bound[a] > x[n]-H_bound[n]) and (n != a) and ((H_bound[n] != m_H_bound) or (V_bound[n] != m_V_bound)):
                                        Overlap = True
                                        break
                                    if (y[a]-V_bound[a] < y[m]+V_bound[m]) and (y[a]+V_bound[a] > y[m]-V_bound[m]) and (x[a]-H_bound[a] < x[m]+H_bound[m]) and (x[a]+H_bound[a] > x[m]-H_bound[m]) and (m != a) and ((H_bound[m] != n_H_bound) or (V_bound[m] != n_V_bound)):
                                        Overlap = True
                                        break
                                
                                if (Overlap == False) :
                                    
                                    #Perhitungan Total Material Handling Cost (TMHC)
                                    TMHC = 0
                                    for a in Allocated :
                                        for b in Allocated :
                                            TMHC = TMHC + Cost[(a,b)]*Flow[(a,b)]*(abs(x_in[a] - x_in[b]) + abs(y_in[a] - y_in[b]))
                                    
                                    #Penentuan pertukaran
                                    if (TMHC < TMHC_opt) :
                                        TMHC_opt = TMHC
                                        m_x_in_opt = x_in[m]
                                        m_y_in_opt = y_in[m]
                                        m_x_opt = x[m]
                                        m_y_opt = y[m]
                                        m_H_bound_opt = H_bound[m]
                                        m_V_bound_opt = V_bound[m]
                                        n_x_in_opt = x_in[n]
                                        n_y_in_opt = y_in[n]
                                        n_x_opt = x[n]
                                        n_y_opt = y[n]
                                        m_opt = m
                                        n_opt = n
                                        n_H_bound_opt = H_bound[n]
                                        n_V_bound_opt = V_bound[n]                   

                                x_in[m] = m_x_in
                                y_in[m] = m_y_in
                                x[m] = m_x
                                y[m] = m_y
                                H_bound[m] = m_H_bound
                                V_bound[m] = m_V_bound
                                x_in[n] = n_x_in
                                y_in[n] = n_y_in
                                x[n] = n_x
                                y[n] = n_y
                                H_bound[n] = n_H_bound
                                V_bound[n] = n_V_bound

        if (TMHC_opt < TMHC_now) :
            TMHC_now = TMHC_opt
            x_in[m_opt] = m_x_in_opt
            y_in[m_opt] = m_y_in_opt
            x[m_opt] = m_x_opt
            y[m_opt] = m_y_opt
            H_bound[m_opt] = m_H_bound_opt
            V_bound[m_opt] = m_V_bound_opt
            x_in[n_opt] =n_x_in_opt
            y_in[n_opt] = n_y_in_opt
            x[n_opt] = n_x_opt
            y[n_opt] = n_y_opt 
            H_bound[n_opt] = n_H_bound_opt
            V_bound[n_opt] = n_V_bound_opt
            
            #Perhitungan TMHC
            TMHC = 0
            for a in Allocated :
                for b in Allocated :
                    TMHC = TMHC + Cost[(a,b)]*Flow[(a,b)]*(abs(x_in[a] - x_in[b]) + abs(y_in[a] - y_in[b]))    
            
            #Visualisasi
            Time = '-'
            plt.figure(figsize=(8,8))
            fig = plt.gcf()
            ax = fig.gca()
            Rect = {}
            Point = {}
            Text = {}
            F_Rect = plt.Rectangle(xy=(0,0), width=F_Length, height=F_Width, color='w')
            ax.add_patch(F_Rect)
            for a in Allocated :
                Rect[a] = plt.Rectangle(xy=(x[a]-H_bound[a],y[a]-V_bound[a]), fill=True, width=2*H_bound[a], height=2*V_bound[a], edgecolor = 'black', fc=Color[a])
                ax.add_patch(Rect[a])
                if (a < 9) :
                    Text[a] = plt.text(x[a]-V_bound[a]/5,y[a]-2*V_bound[a]/3,Label[a])
            for a in Allocated :
                if (a < N+1) :
                    Point[a] = plt.Rectangle(xy=(x_in[a],y_in[a]), fill=True, width=F_Width/150, height=F_Width/150, color='black')
                    ax.add_patch(Point[a])
            plt.text(0,F_Width + 1,'TMHC = ' + str(TMHC))
            plt.text(0,F_Width + 1 + F_Width/40,'Time = ' + str(Time))
            plt.text(F_Length/2,F_Width + 1,'Unallocatable = ' + str(len(Unallocateable)))
            plt.text(F_Length/2,F_Width + 1 + F_Width/40,'Allocated = ' + str(len(Allocated)))
            plt.xlim([0,F_Length])
            plt.ylim([0,F_Width])
            plt.show()
            
        else :
            optimal = True

        print(optimal)

    #Penghapusan dummy batas lantai produksi
    for m in range (N+R+1,N+R+5) :
        Allocated.remove(m)
        del x[m]
        del y[m]
        del x_in[m]
        del y_in[m]
        del H_bound[m]
        del V_bound[m]

    ## Perhitungan TMHC akhir __________________________________________________________________________________________________________
    TMHC_final = 0
    for a in Allocated :
        for b in Allocated :
            TMHC_final = TMHC_final + Cost[(a,b)]*Flow[(a,b)]*(abs(x_in[a] - x_in[b]) + abs(y_in[a] - y_in[b]))

    ## Hentikan perhitungan waktu _______________________________________________________________________________________________________
    end = time.time()
    Time = end - start

    ## Pertimbangan unallocatable __________________________________________________________________________________________________
    after = len(Unallocateable)
    if (len(Unallocateable) == 0) or (after == before) :
        Stop_Allocation = True
    else :
        before = len(Unallocateable)
        for m in Allocated :
            New[m] = 0
        To_Be_Allocated = Allocated + Unallocateable
        Allocated = []
        Unallocateable = []

## Menggambarkan layout setelah alokasi _____________________________________________________________________________________________
plt.figure(figsize=(8,8))
fig = plt.gcf()
ax = fig.gca()
Rect = {}
Point = {}
Text = {}
F_Rect = plt.Rectangle(xy=(0,0), width=F_Length, height=F_Width, color='w')
ax.add_patch(F_Rect)
for a in Allocated :
    Rect[a] = plt.Rectangle(xy=(x[a]-H_bound[a],y[a]-V_bound[a]), fill=True, width=2*H_bound[a], height=2*V_bound[a], edgecolor = 'black', fc=Color[a])
    ax.add_patch(Rect[a])
    Text[a] = plt.text(x[a]-V_bound[a]/5,y[a]-2*V_bound[a]/3,Label[a])
for a in Allocated :
    if (a < N+1) :
        Point[a] = plt.Rectangle(xy=(x_in[a],y_in[a]), fill=True, width=F_Width/150, height=F_Width/150, color='black')
        ax.add_patch(Point[a])
plt.text(0,F_Width + 1,'TMHC = ' + str(TMHC_final))
plt.text(0,F_Width + 1 + F_Width/40,'Time = ' + str(Time))
plt.text(F_Length/2,F_Width + 1,'Unallocatable = ' + str(len(Unallocateable)))
plt.text(F_Length/2,F_Width + 1 + F_Width/40,'Allocated = ' + str(len(Allocated)))
plt.xlim([0,F_Length])
plt.ylim([0,F_Width])
plt.show()

## Export variabel keputusan ________________________________________________________________________________________________________
Sorted_x = dict(sorted(x.items()))
Sorted_y = dict(sorted(y.items()))
Sorted_x_in = dict(sorted(x_in.items()))
Sorted_y_in = dict(sorted(y_in.items()))
Sorted_H_bound = dict(sorted(H_bound.items()))
Sorted_V_bound = dict(sorted(V_bound.items()))
dict_list = [Sorted_x,Sorted_y,Sorted_x_in,Sorted_y_in,Sorted_H_bound,Sorted_V_bound]
index_labels = ['x','y','x_in','y_in','H_bound','V_bound']
df = pd.DataFrame(dict_list, index=index_labels)
df.to_clipboard(index=True, header=True, excel=True)