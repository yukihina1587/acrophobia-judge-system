#define TIMER_TIME 1000

const int heartPin = A1;
int ECG[10] = {0};
int timer_num = 0;
//RRIを出すための配列
int R[2] = {0};
int RRI = 0;
//R値のmsを格納する配列
int timer[10] = {0};
//ピーク値を格納
int peak = 0;
//ピーク値確定フラグ
int R_flag = 0;
//一時的な時間格納
int R_time = 0;
//ミリ秒の獲得
int time_m = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  //心拍を取得
  int heartValue = analogRead(heartPin);
  //タイマーのインクリメントを行う
  m_status_check_handle();
  time_m = millis();

  //取得した最近10個の心拍データを配列に先頭から順に代入
  for(int i = 0; i < 10; i++){
    if(i == 9){
      ECG[i] = heartValue;
      timer[i] = time_m;
      //RRI数値を閾値から割り出す
      if(peak <= ECG[i] && R_flag == 0){
        peak = ECG[i];
        R_time = timer[i];
      }else if((peak - 200) > ECG[i] && (timer[i] - R_time) < 500){
        R_flag = 1;
        if(R_flag == 1){
          peak = 0;
          if(R[0] == 0 && R[1] == 0){
            R[0] = timer[i];
          }else if(R[1] == 0){
            R[1] = timer[i];
          }else{
            R[0] = R[1];
            R[1] = timer[i];
            RRI = R[1] - R[0];
            Serial.print(RRI, DEC);
          }
          R_flag = 0;
        }
      }else if(peak*(7/10) > ECG[i]){
        R_flag++;
      }
    }else{
      ECG[i] = ECG[i+1];
      timer[i] = timer[i+1];
    }
  }
  delay(5);
}

void m_status_check_handle(void){
  timer_num++;
}
/******************************************************************************
  Copyright (C) <2016>  <jianghao>
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
  Contact: hao.jiang@dfrobot.com
 ******************************************************************************/
