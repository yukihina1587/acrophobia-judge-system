/*!
* @file HeartRateMonitor.ino
* @brief HeartRateMonitor.ino  Sampling and ECG output
*
*  Real-time sampling and ECG output
*
* @author linfeng(490289303@qq.com)
* @version  V1.0
* @date  2016-4-5
*/

#include <TimeLib.h>

#define TIME_MSG_LEN 11 // time sync to PC is HEADER followed by Unix time_t as ten ASCII digits
#define TIME_HEADER 'T' // Header tag for serial time sync message
#define TIME_REQUEST 7 // ASCII bell character requests a time sync message 

const int heartPin = A1;
byte j = 0;    //フラグ管理
unsigned long tNow, tPrev;
word peak;
unsigned long time;
long RRI;
int peak_count = 0;    //心拍の拍動間隔(RRI)の個数管理
long sum = 0.0;    //RRIの和
long RR_data[50];    //データを50個格納

void setup() {
  //Serial.println(millis());
  //Serial.println(now());
  Serial.begin(115200);
}

void loop() {
  int heartValue = analogRead(heartPin);
  
  //myPrintf("%02d:%02d:%02d", hour(), minute(), second() );
  /*time = millis();
  Serial.print(time/1000);
  Serial.print("    :    ");
  Serial.println(heartValue*0.005);

  //ピーク時更新なら
  if(heartValue>peak){
    peak = heartValue;    //保存
    tNow=millis();    //時間を取得
    j = 1;    //取得した
  }

  //7割に落ちたときにピーク確定→集計
  if(heartValue<peak*7/10 && j == 1){
    if(peak_count){
      Serial.print("RR:");
      RRI = tNow - tPrev;
      Serial.print(RRI);
      Serial.println("ms");
      sum = sum + RRI;
      calc_SDNN(RRI, sum/peak_count);
    }
  }*/

  /*tPrev = tNow;
  peak = peak*8/10;    //8割以上に上がったら再取得
  peak_count++;
  j = 0;*/
  //Serial.println(heartValue);
  Serial.write(heartValue);
  delay(5);
}

void myPrintf(char *fmt, ...){
  char buf[128];
  va_list args;
  va_start(args, fmt);
  vsnprintf(buf, 128, fmt, args);
  va_end(args);
  Serial.print(buf);
}

void calc_SDNN(long RRI, long ave){
  long sigma = 0.0;
  for(int n = 0; n < peak_count; n++){
    sigma = RRI -  ave;
  }
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
