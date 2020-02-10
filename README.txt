本システムを開発するにあたって必要なソフトウェア
・Arduino IDE 1.8.10（https://www.arduino.cc/en/main/software）
※windowsアプリ版では正常に動作しないことがあるので必ずwindows installer版をインストールしてください。
・ThinkGear Connector（http://developer.neurosky.com/docs/doku.php?id=thinkgear_connector_tgc）
・PyCharm2019.1

本システムを開発するにあたって必要なデバイス
・MindWaveMobile2（EEG測定デバイス）
・Bluetoothコネクタ
・Arduino Uno DFRobot Heart Rate Monitor Sensor

本システムの構成
Arduino Uno DFRobot Heart Rate Monitor Sensor(ECG_get.ino)→(シリアル通信)→Get_ECG.py
MindWaveMobile2→Get_EEG.py
Get_ECG.py、Get_EEG.py→→Get_Value_and_Graph.py

各プログラムの説明
【ECG_get.ino】
ピンから心拍を取得してきてその値を10個の配列に格納する。ピーク値を取得し続け、
ピーク値の7割を切った段階で確定する。同様にして毎回値を取得し、その間隔を取得することで
RRIの数値を獲得する。獲得した値をシリアル通信で送信する。
【Get_ECG.py】
RRIの数値を受信し、配列に格納していく。30個の配列にすべて格納された段階でSDNNとrMSSDの数値を
計算する。最初のSDNN/rMSSDの値を平常値として登録しておき、以降の値は配列に格納し、
multiprocessingのValueとArrayに格納し、渡す。
【Get_EEG.py】Python2.7プログラム
MindWaveから値を取得し、文字列が一致するものを検索し、必要な情報のみを抜き出す。その際に正規表現を
利用してintに変換している。そのデータとヘッダーをローカルホストに送信する。
【Get_Value_and_Graph.py】
Get_EEG.pyからローカルホストで送られてきたデータを受信するメソッドとmultiprocessingで共有した
メモリ内のデータをグラフ化するメソッドに分かれている。グラフ化する際にはmatplotlibを利用している。

本システムを起動するにあたって
本システムを起動するにはPython2.7とPython3.6のコンソールを共存させる必要がある。
https://qiita.com/segur/items/953abf91071632fdae4c
を閲覧し、共存させた上でまずはGet_EEG.pyのプログラムをPython2.7で起動させる。
その上でGet_Value_and_Graph.pyをPython3.6で起動させることでプログラムは作動する。