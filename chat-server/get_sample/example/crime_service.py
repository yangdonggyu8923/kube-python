'''
문제정의 !
서울시의 범죄현황과 CCTV현황을 분석해서
정해진 예산안에서 구별로 다음해에 배분하는 기준을 마련하시오.
예산금액을 입력하면, 구당 할당되는 CCTV 카운터를 자동으로
알려주는 AI 프로그램을 작성하시오.
'''
import os
import sys
from dotenv import load_dotenv
import folium
import numpy as np
from sklearn import preprocessing
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from example.crime_model import CrimeModel
from example.crime_util import Editor, Reader
import pandas as pd
from icecream import ic
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

class CrimeService:

    def __init__(self):
        self.data = CrimeModel()
        self.data.dname = 'C:\\Users\\bitcamp\\python-kube\\chat-server\\get_sample\\example\\data\\'
        self.data.sname = 'C:\\Users\\bitcamp\\python-kube\\chat-server\\get_sample\\example\\save\\'
        self.data.cctv = 'cctv_in_seoul.csv'
        self.data.crime = 'crime_in_seoul.csv'
        self.crime_rate_columns = ['살인검거율', '강도검거율', '절도검거율', '폭력검거율', '강간검거율']
        self.crime_columns = ['살인', '강도', '절도', '폭력', '강간']
        self.arrest_columns = ['살인 검거', '강도 검거', '절도 검거', '폭력 검거', '강간 검거']
        self.crime = []

    def cctv_dataframe(self) -> pd.DataFrame:
        this = self.data
        return pd.read_csv(f'{this.dname}{this.cctv}', encoding='UTF-8', thousands=',')
    
    def crime_dataframe(self) -> pd.DataFrame:
        this =self.data
        return pd.read_csv(f'{this.dname}{this.crime}', encoding='UTF-8', thousands=',')
    
    def save_model(self, fname, dframe: pd.DataFrame) -> pd.DataFrame:
        this = self.data
        return dframe.to_csv(f'{this.sname}{fname}', sep=',', na_rep='NaN')
    
    def save_police_position_master(self) -> None:
        # 아래와 동일한 로직
        crime = self.crime_dataframe()
        reader = Reader()
        gmaps = reader.gmaps(os.environ["api_key"])
        stations = pd.DataFrame(columns=['경찰서명', '위도', '경도', '구별'])
        stations['경찰서명'] = [ '서울' + str(name[:-1]) + '경찰서' for name in crime['관서명']]
        for i in range(len(stations['경찰서명'])):
            tmpMap = gmaps.geocode(stations['경찰서명'][i], language='ko')
            station_addrs = tmpMap[0].get('geometry')
            stations['위도'][i] = station_addrs['location']['lat']
            stations['경도'][i] = station_addrs['location']['lng']
            stations['구별'][i] = [gu['short_name'] for gu in tmpMap[0]['address_components'] if gu['short_name'][-1] == '구'][0]
    
    def save_police_position(self) -> None:
        station_names = []
        crime = self.crime_dataframe()
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1]) + '경찰서')
        station_addreess = []
        station_lats = []
        station_lngs = []
        reader = Reader()
        gmaps = reader.gmaps(os.environ["api_key"])
        for name in station_names:
            t = gmaps.geocode(name, language='ko')
            # print(t)
            station_addreess.append(t[0].get("formatted_address"))
            t_loc = t[0].get("geometry")
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])
        
        gu_names = []
        for name in station_addreess:
            tmp = name.split()
            gu_name = [gu for gu in tmp if gu[-1] == '구'][0]
            gu_names.append(gu_name)
        
        crime['구별'] = gu_names
        # 구 와 경찰서의 위치가 다른 경우 수작업
        crime.loc[crime['관서명'] == '혜화서', ['구별']] = '종로구'
        crime.loc[crime['관서명'] == '서부서', ['구별']] = '은평구'
        # crime.loc[crime['관서명'] == '강서서', ['구별']] = '양천구'
        crime.loc[crime['관서명'] == '종암서', ['구별']] = '성북구'
        crime.loc[crime['관서명'] == '방배서', ['구별']] = '서초구'
        crime.loc[crime['관서명'] == '수서서', ['구별']] = '강남구'
        crime.to_csv(f'{self.data.sname}police_position.csv')
        
    def save_cctv_population(self) -> None:
        reader = Reader()
        population = reader.excel(f'{self.data.dname}pop_in_seoul', 2, 'B, D, G, J, N')
        cctv = self.cctv_dataframe()
        cctv.rename(columns={cctv.columns[0] : '구별'}, inplace=True) # inplace=True 원본을 수정하겠다.
        population.rename(columns={population.columns[0] : '구별',
                                   population.columns[1] : '인구수',
                                   population.columns[2] : '한국인',
                                   population.columns[3] : '외국인',
                                   population.columns[4] : '고령자'}, inplace=True)
        
        ic(population.head(2))
        ic(cctv.head(2))
        #population에서 Nan값이 있는지 확인 후 제거하세요
        population.drop([26], axis=0, inplace=True) #26번째 행을 제거, axis=0은 행을 의미, axis=1은 열을 의미
        population['외국인비율'] = population['외국인'].astype(int) / population['인구수'].astype(int) * 100 #외국인비율을 구하는 공식
        population['고령자비율'] = population['고령자'].astype(int) / population['인구수'].astype(int) * 100 #고령자비율을 구하는 공식
        cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], axis=1, inplace=True) #열을 제거
        cctv_per_populations = pd.merge(cctv, population, on='구별') # on='구별'을 기준으로 병합
        cor1 = np.corrcoef(cctv_per_populations['고령자비율'], cctv_per_populations['소계']) # 상관계수를 구하는 함수
        cor2 = np.corrcoef(cctv_per_populations['외국인비율'], cctv_per_populations['소계'])
        ic(f'고령자비율과 CCTV의 상관계수 {str(cor1)} \n'
              f'외국인비율과 CCTV의 상관계수 {str(cor2)} ')
        """
         고령자비율과 CCTV 의 상관계수 [[ 1.         -0.28078554]
                                     [-0.28078554  1.        ]] 
         외국인비율과 CCTV 의 상관계수 [[ 1.         -0.13607433]
                                     [-0.13607433  1.        ]]
        r이 -1.0과 -0.7 사이이면, 강한 음적 선형관계,
        r이 -0.7과 -0.3 사이이면, 뚜렷한 음적 선형관계,
        r이 -0.3과 -0.1 사이이면, 약한 음적 선형관계,
        r이 -0.1과 +0.1 사이이면, 거의 무시될 수 있는 선형관계,
        r이 +0.1과 +0.3 사이이면, 약한 양적 선형관계,
        r이 +0.3과 +0.7 사이이면, 뚜렷한 양적 선형관계,
        r이 +0.7과 +1.0 사이이면, 강한 양적 선형관계
        고령자비율 과 CCTV 상관계수 [[ 1.         -0.28078554] 약한 음적 선형관계
                                    [-0.28078554  1.        ]]
        외국인비율 과 CCTV 상관계수 [[ 1.         -0.13607433] 거의 무시될 수 있는
                                    [-0.13607433  1.        ]]                        
         """
        cctv_per_populations.to_csv(f'{self.data.sname}cctv_population.csv')

    def save_crime_arrest_normalization(self) -> None:
        reader = Reader()
        # crime = self.crime_dataframe()
        
        police_position = reader.csv(f'{self.data.sname}police_position')
        police = pd.pivot_table(police_position, index='구별', aggfunc=np.sum)
        ic(police)
        police['살인검거율'] = police['살인 검거'].astype(int) / police['살인 발생'].astype(int) * 100
        police['강도검거율'] = police['강도 검거'].astype(int) / police['강도 발생'].astype(int) * 100
        police['강간검거율'] = police['강간 검거'].astype(int) / police['강간 발생'].astype(int) * 100
        police['절도검거율'] = police['절도 검거'].astype(int) / police['절도 발생'].astype(int) * 100
        police['폭력검거율'] = police['폭력 검거'].astype(int) / police['폭력 발생'].astype(int) * 100
        police.drop(['강간 검거', '강도 검거', '살인 검거', '절도 검거', '폭력 검거'], axis=1, inplace=True)
        
        for i in self.crime_rate_columns:
            police.loc[police[i] > 100, i] = 100
            
        police.rename(columns={'강간 발생':'강간',
                               '살인 발생':'살인',
                               '절도 발생':'절도',
                               '폭력 발생':'폭력',
                               '강도 발생':'강도'}, inplace=True)
        print('loc 결과 : ')
        ic(police)
        x = police[self.crime_rate_columns].values
        min_max_scalar = preprocessing.MinMaxScaler()
        """   
        피쳐 스케일링(Feature scalining)은 해당 피쳐들의 값을 일정한 수준으로 맞춰주는 것이다.
        이때 적용되는 스케일링 방법이 표준화(standardization) 와 정규화(normalization)다.
        
        1단계: 표준화(공통 척도)를 진행한다.
            표준화는 정규분포를 데이터의 평균을 0, 분산이 1인 표준정규분포로 만드는 것이다.
            x = (x - mu) / sigma
            scale = (x - np.mean(x, axis=0)) / np.std(x, axis=0)
        2단계: 이상치 발견 및 제거
        3단계: 정규화(공통 간격)를 진행한다.
            정규화에는 평균 정규화, 최소-최대 정규화, 분위수 정규화가 있다.
             * 최소최대 정규화는 모든 데이터를 최대값을 1, 최솟값을 0으로 만드는 것이다.
            도메인은 데이터의 범위이다.
            스케일은 데이터의 분포이다.
            목적은 도메인을 일치시키거나 스케일을 유사하게 만든다.     
        """
        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        police_norm = pd.DataFrame(x_scaled, columns=self.crime_rate_columns, index=police.index)
        police_norm[self.crime_columns] = police[self.crime_columns]
        police_norm['범죄'] = np.sum(police_norm[self.crime_rate_columns], axis=1)
        police_norm['검거'] = np.sum(police_norm[self.crime_columns], axis=1)
        police_norm.to_csv(f'{self.data.sname}police_norm.csv', sep=',', encoding='UTF-8')

    def folium_test(self):
        reader = Reader()
        state_geo = reader.json(f'{self.data.dname}us-states')
        state_data = reader.csv(f'{self.data.dname}us_unemployment')

        m = folium.Map(location=[48, -102], zoom_start=3)

        folium.Choropleth(
            geo_data=state_geo,
            name="choropleth",
            data=state_data,
            columns=["State", "Unemployment"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Unemployment Rate (%)",
        ).add_to(m)
        folium.LayerControl().add_to(m)
        m.save(f'{self.data.sname}us_states.html')
    
    def draw_crime_map(self):
        reader = Reader()
        state_geo = reader.json(f'{self.data.dname}kr-states')
        state_data = reader.csv(f'{self.data.sname}police_norm') # 정규화한 데이터
        m = folium.Map(location=[37.5502, 126.982], zoom_start=12, title="Stamen Toner")
        police_position = reader.csv(f'{self.data.sname}police_position')
        police_norm = reader.csv(f'{self.data.sname}police_norm')
        crime = self.crime_dataframe()
        station_names = []
        for name in crime['관서명']:
            sample = '서울' + str(name[:-1]) + '경찰서'
            # print(f'---> {sample}')
            station_names.append(sample)
        station_addreess = []
        station_lats = []
        station_lngs = []
        gmaps = reader.gmaps(os.environ["api_key"])
        for i, name in enumerate(station_names):
            temp = gmaps.geocode(name, language='ko')
            # if name == '서울강서경찰서':
            #     print('서울강서경찰서 위치가 정확하지 않아 수동으로 입력합니다.')
                
            # else:
            #     print('서울종암경찰서 위치가 정확하지 않아 수동으로 입력합니다.')
            #     temp = self.jongam_police_info()
            station_addreess.append(temp[0].get("formatted_address"))
            t_loc = temp[0].get("geometry")
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])
        police_position['lat'] = station_lats
        police_position['lng'] = station_lngs

        temp = police_position[self.arrest_columns] / police_position[self.arrest_columns].max()
        police_position['검거'] = np.sum(temp, axis=1)

        folium.Choropleth(
            geo_data=state_geo,
            name="choropleth",
            data=tuple(zip(police_norm['구별'], police_norm['범죄'])),
            columns=["State", "Crime Rate"],
            key_on="feature.id",
            fill_color="PuRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Crime Rate (%)",
        ).add_to(m)
        
        for i in police_position.index:
            folium.CircleMarker([police_position['lat'][i], police_position['lng'][i]],
                          radius=police_position['검거'][i] * 10,
                          fill_color='#0a0a32').add_to(m) # 지도에 원 추가
            
        folium.LayerControl().add_to(m)
        m.save(f'{self.data.sname}kr_states.html')
    
if __name__ == '__main__':
    service = CrimeService()
    cctv_df = service.cctv_dataframe()
    crime_df = service.crime_dataframe()
    # ic(cctv_df)
    # ic(crime_df)
    # service.save_police_position()
    # service.save_cctv_population()
    service.save_crime_arrest_normalization()
    # service.draw_crime_map()
