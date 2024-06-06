# Tanegashima_Rocket_Contest_2024_Runback
![](https://img.shields.io/badge/release_date-May_2024-yellow)
![](https://img.shields.io/badge/python-v3.9.2-blue)
![](https://img.shields.io/badge/OpenCV-v4.7.0-blue)
![](https://img.shields.io/badge/os-linux11-blue)  
![](https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat)
![](https://img.shields.io/badge/-Linux-6C6694.svg?logo=linux&style=flat)
![](https://img.shields.io/badge/-Raspberry%20Pi-C51A4A.svg?logo=raspberry-pi&style=flat)  

This is a project of Team Astrum, CanSat and Runback Division of Tanegashima Rocket Contest 2024. 


## Mission  
The drone is dropped from 30 m above the ground, decelerated by a parachute, and lands on the ground. The drone aims for a zero-distance goal to a pylon placed at the goal point under autonomous control.  
  
## Mission Sequence  
The program starts when the carrier is loaded, and judges the ascent and landing by the air pressure sensor. In case of a sensor error, the landing judgment is also made over time. After landing, the separation mechanism is activated, and the CanSat uses the geomagnetic sensor and GPS to reach the goal. After approaching the goal, the camera starts image processing and distance measurement, and the program terminates when it judges that the goal has been reached.

## Success Criteria  

| | 内容 |評価方法|
| ---- | ---- |---|
| Minimum Success |機体の損傷のない着地|目視での確認|
| Full Success |パンタグラフの展開<br>カメラによるゴールの識別|目視と制御履歴による確認|
| Extra Success |ゼロ距離ゴール|目視と制御履歴による確認|


## Software Configuration
Language : Python 3.9.2  
OS       : Raspberry Pi OS Lite (32-bit)   
Raspbian GNU/Linux 11 (bullseye)    
Kernel   : Ver.5.15    
OpenCV   : Ver.4.7.0    

## Hardware Configuration

Computer                   : Raspberry pi4  
GPS                        : GYSFDMAXB  
9-axis sensor              : BNO055  
Barometric pressure sensor : BME280  
Camera                     :   
Motor Driver               : BD6231F  

<img src="https://github.com/Yuzudayo/Noshiro_Space_Event_2023/assets/89567103/0f004150-3715-4827-bc23-d73a55e51d5f" width="450px">

## Program Configuration

- main.py  
    メインプログラム．ミッションシーケンスのフローに従って動作する．
- fallback.py  
    フォールバック用のプログラム．ラズベリーパイが再起動してしまった際に自動的に起動するようになっており，メインプログラムの分離機構作動後の動作を行う．
- logger.py  
    ログのクラスを定義する．各フェーズ及びエラー時のログを作成し，csv形式で出力する．
- floating.py  
    高度を計算するために用いる．bme280モジュールから気圧と温度を取得し，初期高度に対する相対高度を計算する．
- ground.py  
    地上走行フェーズで使用するプログラム．地磁気やGPSの情報からゴールまでの距離や角度を算出し，機体の制御を決定する．
- bme280.py  
    BME280を用いて気圧と温度のデータを取得する．
- GYSFDMAXB.py  
    GPSモジュールから緯度経度を毎秒取得する．取得プログラムはデーモンで動作する．
- bno055.py  
    BNO055から気圧と加速度のデータを取得する．各値は内蔵されているマイコンで自動的にキャリブレーションされ，その度合いも確認できる．
- img_proc.py  
    画像処理のモジュールであり，写真を撮って，得られた画像の色情報から赤いパイロンを検出する.
- motor.py  
    モーター類を扱うクラスで，タイヤやパンタグラフ展開モーターを制御する．また，分離機構用のサーボモーターも制御する．

## Result
1回目，2回目においてはMinimum Successを達成し，3回目はFull Successを達成した．ゴールまでの距離としては，3回目の約4mが最高記録である．  
### １回目
ドローン浮上と同時に高度の値が大幅に下がり，エラー検出したため，時間経過による着地判定(15分後)に移行した．投下時，キャリアにスタビライザーが引っ掛かったが，ドローンを揺らすことによって投下に成功した．着地はうまくいったように見られたが，15分経過しても機体が動作せず，リタイアとなった．ログを確認してみたところ，エラー検出の履歴はあったが，着地判定をした履歴が見当たらず，再起動した様子やプログラムのバグもないので，原因は不明のままである．着地判定の時間が長く感じられたため，8分に短縮し，センサの異常もカウンターを用意し，15回の異常検知でエラーとした．また，上昇検知や着地判定の閾値も変更して外れ値に対応できるようにし，エラー検出後もセンサの値をログに取るようにした．標準出力と標準エラー出力もファイルに書き出すようにした．
### ２回目
キャリアからスムーズに投下でき，着地判定も正常に動作してパラシュートを分離，走行を開始できた．しかし，パラシュート上でスタック処理をしたため，右側のタイヤがパラシュートに絡まり，走行不能とみなしてリタイアとなった．前進した際はパラシュートに絡まらないことや，パラシュートがパトロンの色と酷似しているため，パラシュートに対する処理を考慮していなかった．これを受け，地上から4m付近でパラシュートをすぐに分離し，パラシュートから距離をとるために15秒ほど前進する処理を追加した．

<img src="https://github.com/Yuzudayo/Noshiro_Space_Event_2023/assets/89567103/7b029a0f-fac1-4bab-acb1-c3a1149a5c3c" width=380px>

<img src="https://github.com/Yuzudayo/Noshiro_Space_Event_2023/assets/89567103/a80d2084-e960-4618-b798-29e2f6f43e80" width=380px>

### ３回目

<img src="https://github.com/Yuzudayo/Noshiro_Space_Event_2023/assets/89567103/1fb89a98-006b-47dc-9ffa-c8026b6289eb" width=450px>

実装した通り，地上4m付近で分離機構が作動し，パラシュートと絡まらずに走行を開始した．何度かスタックしながらもゴール8m付近まで接近し，画像処理フェーズに移行した．何度かゴールを検知したが，スタック判定に入ったり，機体が横転したりして思うように進まず，ゴールまで4mのところで開始から15分経過し，時間切れとなった．

<img src="https://github.com/Yuzudayo/Noshiro_Space_Event_2023/assets/89567103/dfdcdf8b-0dfe-4584-805c-b23eaf3da2e0" height=300px>

<img src="https://github.com/Yuzudayo/Noshiro_Space_Event_2023/assets/89567103/b9dd28c4-5596-416a-aa42-a86fcb0f4844" height=300px>

## Comment  
フィールドの状態が想定よりも悪く(草木の刈り残しが多かった)，機体がスタックしたり，走行不可能になったりしたため，環境に対応するため，直前に様々な変更に追われた．スタック判定においても，加速度による機体の姿勢から判定していたが，誤検知も多く見られたため，変更した方がいいと思った．  
画像処理フェーズにおいて，直前の変更諸々や時間が足りず，うまくスタック判定や制御ができていなかったと思う．周辺環境に赤いものが散見されることや，色情報によるパトロンの識別に限界があることから，計算処理用のモジュールを追加し，機械学習を用いた方が確実だと感じた．  
mainプログラムにおいても，前大会の使い回しで冗長な部分があり，改善点が多く見受けられた．ログのクラス定義の部分も，エラー検出やバグをなくすために修正できる部分が見受けられた．  
全体を通して，デバッグやレビューが足りず，リファクタリングが必要であると感じた．また，実機を用いた試験をより行い，スタック処理や画像処理フェーズの動きなど，改善できる部分が多くあると思った．
