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

void setup() {
  //Serial.println(millis());
  //Serial.println(now());
  Serial.begin(115200);
}

void loop() {
  //myPrintf("%02d:%02d:%02d", hour(), minute(), second() );
  int heartValue = analogRead(heartPin);
  Serial.println(heartValue);
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
