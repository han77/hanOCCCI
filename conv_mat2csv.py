import scipy.io
import pandas as pd
import os
import mat73
import numpy as np

def read_hyc_ocean_lola():
    file = 'D:\\Study\\mattest\\hyc_ocean_lola.mat'
    
    try:
        mat = scipy.io.loadmat(file)
    except NotImplementedError:
        mat = mat73.loadmat(file)
    except:
        ValueError('could not read at all....')
    
    #dict_keys(['__header__', '__version__', '__globals__', 'lat', 'lon'])
    data = [mat[k] for k in list(mat.keys()) if k == 'lon' or k == 'lat']
    lat = data[0]        
    lon = data[1]
    return list([lon,lat])

def read_ncep_wnd_lola():
    file = 'D:\\Study\\mattest\\ncep_wnd_lola.mat'
    
    try:
        mat = scipy.io.loadmat(file)
    except NotImplementedError:
        mat = mat73.loadmat(file)
    except:
        ValueError('could not read at all....')
    
    #dict_keys(['__header__', '__version__', '__globals__', 'lat', 'lon'])
    data = [mat[k] for k in list(mat.keys()) if k == 'lonw' or k == 'latw']
    lon = data[0]
    lat = data[1]        
    return list([lon,lat])

def conv_mat2csv(input_dir, input_filename, output_dir, output_filename):
    matf = os.path.join(input_dir, input_filename)
    csvf = os.path.join(output_dir, output_filename)
    
    #한번 만든 csv는 넘어간다.    
    if os.path.exists(csvf):
        print("있어서 그냥 넘어가요.")
        return False
    #보조자료는 넘어간다.    
    if input_filename == 'hyc_ocean_lola.mat' or input_filename == 'ncep_wnd_lola.mat':
        print("보조자료라서 넘어가요.")
        return False
    

    try:
        mat = scipy.io.loadmat(matf)
    except NotImplementedError:
        mat = mat73.loadmat(matf)
    except:
        ValueError('could not read at all....')

    # input folder의 정보는 다르네.
    if "input" in input_dir:
        if "wind" in input_dir:
            print("input,wind 정보네요")

            data = [mat[k] for k in list(mat.keys()) if k == 'uw' or k == 'vw']
            dfu = pd.DataFrame(data[0])
            dfv = pd.DataFrame(data[1])
            tdfu = dfu.T 
            tdfv = dfv.T 

            #폴더가 없을 때 생성
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            #size 121 x 93 -> 93x 121 - >1차원
            # u_index = ['u'+ str(item) for item in list(range(0,121))]
            # v_index = ['v'+ str(item) for item in list(range(0,121))]
            # tdfu.to_csv(path_or_buf=csvf, header=u_index, index=True, sep=',',mode='w' )
            # tdfv.to_csv(path_or_buf=csvf, header=v_index, index=True, sep=',',mode='a' )
               
            
            # lon lat u v 로 저장하기
            ll = read_ncep_wnd_lola()
            wndlon = ll[0] #size 93x121
            wndlat = ll[1] #size 93x121

            # for lon, lat, u, v in zip(wndlon, wndlat, tdfu, tdfv):
            #     print(lon, lat, u, v)
            a1 = np.array(wndlon)
            a2 = np.array(wndlat)
            a3 = np.array(tdfu)
            a4 = np.array(tdfv)
            a11 = a1.flatten()
            a22 = a2.flatten()
            a33 = a3.flatten()
            a44 = a4.flatten()
            marr = np.vstack((a11, a22, a33, a44))
            ddf = pd.DataFrame(marr)
            tddf = ddf.T
            tddf.to_csv(path_or_buf=csvf, header=['Lon','Lat', "wndu", "wndv"], index=False, sep=',',mode='w')

            print("### 저장 완료", csvf) 

        elif "ECS_ct" in input_filename:
            print("input,해류 정보네요")
            data = [mat[k] for k in list(mat.keys()) if k == 'uu' or k == 'vv']
            dfu = pd.DataFrame(data[0])
            dfv = pd.DataFrame(data[1])
            tdfu = dfu.T 
            tdfv = dfv.T 
            #폴더가 없을 때 생성
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            #size 576 x 376
            u_index = ['u'+ str(item) for item in list(range(0,376))]
            v_index = ['v'+ str(item) for item in list(range(0,376))]
            tdfu.to_csv(path_or_buf=csvf, header=u_index, index=True, sep=',',mode='w' )
            tdfv.to_csv(path_or_buf=csvf, header=v_index, index=True, sep=',',mode='a' )


            print("### 저장 완료", csvf) 
        else:    
            print("input,GOCI 정보네요")
            data = [mat[k] for k in list(mat.keys()) if k == 'lon' or k == 'lat']
            df = pd.DataFrame(data)
            tdf = df.T 
            #폴더가 없을 때 생성
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            tdf.to_csv(path_or_buf=csvf, header=['lon','lat'], index=False, sep=',',mode='w' )
            print("### 저장 완료", csvf)                

    else:
    # output file 처리(예측정보들)
        # print(mat.keys())
    #  dict_keys(['P_age', 'P_age_end', 'Xp_end', 'Xp_lon', 'Yp_end', 'Yp_lat', 'Zp', 'dfinish', 'dnum', 'dstart', 'dt', 'el_t', 'it', 'iti', 'll', 'log_p', 'npar'])

        # print(mat)
        # your_data = mat['P_age', 'P_age_end', 'Xp_end', 'Xp_lon', 'Yp_end', 'Yp_lat', 'Zp', 'dfinish', 'dnum', 'dstart', 'dt', 'el_t', 'it', 'iti', 'll', 'log_p', 'npar']
        # df = pd.DataFrame(your_data)
        # df.to_csv(csvf)

        data = [mat[k] for k in list(mat.keys()) if k == 'Xp_lon' or k == 'Yp_lat']
        df = pd.DataFrame(data)
        tdf = df.T

        #폴더가 없을 때 생성
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        tdf.to_csv(path_or_buf=csvf, header=['Xp_lon','Yp_lat'], index=False, sep=',',mode='w' )
        print("%s 저장 완료", csvf)                

    return 1

def conv():
    main_path = 'D:\\Study\\mattest\\'

    #폴더 아래 mat 파일 모두 찾기
    count = 0
    for (path, dir, files) in os.walk(main_path):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.mat':
                print("%s : %s \ %s, exists(%s)" % (count, path, filename, os.path.exists(os.path.join(path,filename))))
                count += 1

                idir = path 
                ifile = filename
                odir = os.path.join(idir, 'csv')
                if os.path.isfile(os.path.join(idir, ifile)) == True:
                    name, ext = os.path.splitext(ifile)
                    ofile = name+ '.csv'

                    ret = conv_mat2csv(idir, ifile, odir, ofile)
                    

#테스트로 하나만  실행해 보기
# file ='D:\\Study\\mattest\\build_SG_20210408_FT_forecast_from20210408\\output_2021\\2021\\Sar_ex_200325_hycom_2021_040809.mat'
#file = "D:\\Study\\mattest\\input_20210407\\s1_0_wind\\gfs_20210407_0012_000.mat"

# idir = os.path.dirname(file)
# ifile = os.path.basename(file)
# os.path.isfile(os.path.join(idir, ifile))
# name, ext = os.path.splitext(ifile)
# odir = os.path.join(idir, 'csv')
# ofile = name+ '.csv'

# ret = conv_mat2csv(idir, ifile, odir, ofile)

# matf = ''
# csvf = matf+'.csv'
# mat = scipy.io.loadmat(matf)
# your_data = mat['xx']
# df = pd.DataFrame(your_data)
# df.to_csv(csvf)

    return

# ll = read_hyc_ocean_lola()

# hyclon = ll[0]
# hyclat = ll[1]

# file = "D:\\Study\\mattest\\input_20210407\\s1_1_ct\\ECS_ct_2021040712.mat"
# mat = scipy.io.loadmat(file)
# data = [mat[k] for k in list(mat.keys()) if k == 'uu' or k == 'vv']
# dfu = pd.DataFrame(data[0])
# dfv = pd.DataFrame(data[1])
# tdfu = dfu.T 
# tdfv = dfv.T 
# for lon, lat, u, v in zip(hyclon, hyclat, tdfu, tdfv):
#     print(lon, lat, u, v)
# a1 = np.array(hyclon)
# a2 = np.array(hyclat)
# a3 = np.array(tdfu)
# a4 = np.array(tdfv)
# a11 = a1.flatten()
# a22 = a2.flatten()
# a33 = a3.flatten()
# a44 = a4.flatten()
# marr = np.vstack((a11, a22, a33, a44))
# ddf = pd.DataFrame(marr)
# tddf = ddf.T
# tddf.to_csv(path_or_buf=file+'.csv', header=['Lon','Lat', "wndu", "wndv"], index=False, sep=',',mode='w' )





