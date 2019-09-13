#define TIMER_TIME 1000

const int heartPin = A1;
int ECG[10] = {0};
int timer_num = 0;
//RRIを出すための配列
int R[2] = {0};
int RRI = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  //心拍を取得
  int heartValue = analogRead(heartPin);
  //タイマーのインクリメントを行う
  m_status_check_handle();

  //取得した最近10個の心拍データを配列に先頭から順に代入
  for(int i = 0; i < 10; i++){
    if(i == 9){
      ECG[i] = heartValue;
    }else{
      ECG[i] = ECG[i+1];
    }
  }

  //RRI数値を閾値から割り出す
  if(ECG[10] - ECG[9] > 100){
    R[0] = R[1];
    R[1] = timer_num;
    RRI = R[1] - R[0];
  }

  Serial.write(RRI);
  //Serial.println(RRI);
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
