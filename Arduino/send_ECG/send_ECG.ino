const int heartPin = A1;
int timer_num = 0;
//一時的な時間格納
int R_time = 0;
//ピーク値確定フラグ
int R_flag = 0;
//ピーク値を格納
int peak = 0;
//RRIを出すための配列
int R[2] = {0};
int RRI = 0;
//R値のmsを格納する配列
int timer[10] = {0};
int ECG[10] = {0};

void setup() {
  Serial.begin(9600);
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
      timer[i] = timer_num;
      if(peak <= ECG[i] && R_flag == 0){
        peak = ECG[i];
        Serial.println(peak);
        R_time = timer[i];
        Serial.println(timer[i] - R_time);
        Serial.println(peak - ECG[i]);
      }else if(timer[i] - R_time < 25 && peak - ECG[i] > 200){
        //ピーク値確定
        R_flag = 1;
        if(R_flag == 1){
          peak = 0;
          if(R[0] == 0 && R[1] == 0){
            R[0] = R_time;
          }else if(R[1] == 0){
            R[1] = R_time;
          }else{
            R[0] = R[1];
            R[1] = R_time;
            RRI = R[1] - R[0];
            Serial.println(RRI, DEC);
          }
        }
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
