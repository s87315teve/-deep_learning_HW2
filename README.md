# Deep learning kaggle02 (學號409504010)

* step 0: 前置作業
參考[kaggle01](https://github.com/s87315teve/deep_learning_HW1)建立環境
* step 1: 下載本次作業所需noise資料
    * https://www.openslr.org/17 (musan)
    * https://mcdermottlab.mit.edu/Reverb/IR_Survey.html (Audio)
    * http://www.echothief.com (EchoThiefImpulseResponseLibrary)
* step 2: 建立data_augmentation資料夾並將下載的檔案移動到指定位置
```
mkdir data_augmentation
cd data_augmentation
mkdir backfround_noises
mkdir rir
mkdir short_noises
cd ..
mv musan/music/ data_augmentation/backfround_noises/
mv musan/noise/sound-bible/ data_augmentation/short_noises/
mv Audio/ data_augmentation/rir/
mv EchoThiefImpulseResponseLibrary/ rir/
```
* step 3: 將其他需要使用到的檔案移動到data_augmentation資料夾
    * audio_augmentation.py
    * dataset_split.py
    * transript_augmentation.py
    * train資料夾 (train dataset)
    * aishell_transcript.txt (先把原本底下test的部分移除)
* step 4: 安裝環境 (可能會有相關套件的版本問題)
執行espnet/tools/installers中的install_s3prl.sh和install_fairseq.sh來安裝套件(會有版本衝突，需注意)
```
./install_s3prl.sh
./install_fairseq.sh
```
安裝python的audiomentations以供資料增強使用
```
pip install audiomentations
```
* step 5: data augmentation
執行audio_augmentation.py，會輸出一個資料夾是train_augmentation，裡面有加完雜訊的檔案
```
python audio_augmentation.py
```
執行完audio_augmentation.py後，把train_augmentation的檔案全部都移動到train資料夾裡

接下來把aishell_transcript.txt檔案名稱改成aishell_transcript_origin.txt，並執行transcript_augmentation.py輸出新的aishell_transcript.txt
```
python transcript_augmentation.py
```
之後再把原本檔案test的部分加回aishell_transcript.txt的最底下

執行dataset_split.py將train資料夾裡面的dataset分成train set和dev set，移動到對應的資料夾內以供訓練，目前預設是拿80%當作train set，20%當作dev set   (執行時要注意程式裡面的路徑)
```
dataset_split.py
```

最後再把aishell_transcript.txt移動到對應的位置即可

* step 6: 使用新的config檔案
把espnet/egs2/librispeech/asr1/conf/tuning/train_asr_conformer7_wavlm_large.yaml移動至espnet/egs2/aishell/asr1/conf/tuning/中，並把train_asr_conformer7_wavlm_large.yaml中frontend和preencoder的部分修改為使用wavlm_large的模型，更改內容如下:

```yaml
frontend: s3prl
frontend_conf:
    frontend_conf:
        upstream: wavlm_large  # Note: If the upstream is changed, please change the input_size in the preencoder.
    download_dir: ./hub
    multilayer_feature: True
```
preencoder的部分則是把input size改成768

改完後再到asr.sh中把模型換成train_asr_conformer7_wavlm_large.yaml
* step 7: 開始訓練
```
./run.sh -feats_normalize uttmvn
```



---
## 調參數與model結果

在本次kaggle競賽中，嘗試了以下參數來訓練模型
| case | 模型 | 參數 | train:dev | epoch |score|
| --- | --- | --- | --- | --- | --- |
| case1 | conformer7_wavlm_large| lr: 0.0025 <br>batch_bins: 1000000 | 2919 : 200 | 35 |**latest** 12.49514|
| case2 | conformer7_wavlm_large| lr: 0.0015 <br>batch_bins: 1000000 | 2919 : 200 | 80 |**latest** 11.28155|
| case3 | conformer7_wavlm_large| lr: 0.0015 <br>batch_bins: 1500000 | 4990 : 1248 | 80 |**latest** 8.02912<br>**best** 7348543<br>**10best** <font color="red">5.80582</font>
