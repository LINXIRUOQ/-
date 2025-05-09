通过YOLO/opencv识别实现常规验证码自动验证<br>
环境：<br>
python3<br>
服务器：ubuntu（如果本地部署则不需要）<br>
框架：flask（如果本地部署则不需要）<br>
数据库：mysql（如果本地部署则不需要）<br>
<br>
项目耗时：5天<br>
预计部署耗时：1天<br>
<br>
使用到的项目：<br>
-YOLO11#物体检测/分割<br>
https://docs.ultralytics.com/zh/models/yolo11/<br>
-CnOcr#文字识别<br>
https://cnocr.readthedocs.io/zh-cn/latest/<br>
-yolo打标工具<br>
https://github.com/HumanSignal/labelimg<br>
-yolo数据增删改：可见我主页上一个项目<br>
-BurtSuipe<br>
抓包教程链接：<br>
<br>
https://blog.csdn.net/m0_46607055/article/details/137638350?spm=1001.2101.3001.6650.17&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7Ebaidujs_baidulandingword%7ECtr-17-137638350-blog-140867877.235%5Ev43%5Epc_blog_bottom_relevance_base4&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7Ebaidujs_baidulandingword%7ECtr-17-137638350-blog-140867877.235%5Ev43%5Epc_blog_bottom_relevance_base4&utm_relevant_index=20
项目流程：<br><br>
说明：{}内为文件夹路径，或py文件<br>
1--<br><br>
    使用BurtSuipe抓包获取验证码网址{BurtSuipe1.png}，分析抓包链接，获得请求产生例：{请求参数.txt}，拿到{BurtSuipe2.png}链接，通过分析测试可知vtype为验证码类别，修改url链接获取不同验证码。<br>拼接后网址链接为：https://xyq-service.netease.com/vweb/verification?vtype=2&server=https%3A%2F%2Fsm-g85-15xa39t8-prod-ws.nie.netease.com%3A12004%2Fxyq_service%2Fxyq-verification%2F&retry=2&umark=eyJob3N0aWQiOiAiMzAwMDAiLCAidmVyaWZ5X3R5cGUiOiAiZmFybSIsICJhaWQiOiAiOTA3MDU0MyIsICJjbGllbnRfaWQiOiAwLCAiY2hhcl9pZCI6ICIxMDAxMjIyMDQ5MSJ9&callback=default&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhaWQiOiI5MDcwNTQzIiwiY29uZmlnIjp7ImFwcGlkIjoic20tZzg1LTE1eGEzOXQ4In0sImV4cCI6MTc0NzEyNjgzNSwiZ2FtZV9pZCI6Imc4NSIsImlhdCI6MTc0NjUyMjAzNSwidGNwIjp7ImFkZHIiOiI0NS4yNTMuMTY5LjIwNToxMjEwMSIsInJjNCI6dHJ1ZSwidGxzIjpmYWxzZX0sIndlYnNvY2tldCI6eyJhZGRyIjoic20tZzg1LTE1eGEzOXQ4LXByb2Qtd3MubmllLm5ldGVhc2UuY29tOjEyMTA0IiwidGxzIjp0cnVlfX0.KXCnF2ggcBC9n4Dnv5W949_txFZbXh1OXIc5LD3cFPs<br>
2--<br><br>
    使用代码{自动刷新截图图片下载.py}获取大量数据，使用{labelImg}等软件进行数据标注<br>
    配置YOLO训练环境{python环境}<br>
    下载YOLO模型<br>
    --使用11n/11m/yolo11m-cls模型<br>
3--图像验证码：<br><br>
    形状验证码通常包含大量形状，朝向，颜色<br>
    复杂度：（26+10+8）*3*7=924<br>
    这个标签数量显然不是一个人能完成的，故将yolo模型拆分为形状，颜色，朝向三个模型，并结合opencv来对图片预处理保证图片能完美识别以求最小的人工标注量。<br>
    形状识别：<br>
    --小模型/数据集足够：<br>
    文件夹：{./YOLO训练/图形识别模型训练}，配置{icon.yaml}，将修为自己的训练集和验证集，使用代码{1训练.py}训练yolo，训练完毕，使用{3识别（视频测试）.py}验证训练模型的结果<br>
    --大模型/需大量数据集：<br>
    文件夹：{./YOLO训练/图形识别模型训练}，配置{icon.yaml}，将修为自己的训练集和验证集，使用代码{1训练.py}训练yolo，训练完毕，使用{3识别（视频测试）.py}验证训练模型的结果，使用循环号的bast.pt文件和{2使用模型自动标注yolo训练数据.py}对未标注的数据进行自动标注，使用{labelImg}验证标注进行校准，{https://github.com/LINXIRUOQ/labelImg-sorted.git}整删改提纯数据。再次训练yolo，验证，标注直至数据集够大训练出满意的.pt模型<br>
    朝向识别：<br><br>
    文件夹：{.\YOLO训练\分类训练}使用{1使用图形训练后的.bt文件，处理图像制作并分割单个分割图像文件.py}和形状识别训练后的{bast.pt}模型,将图像素材进行分割，分割完后使用[2分类训练.py]进行朝向模型的训练注意选择{yolo11m-cls}分类模型，训练完成后使用{3识别（处理文件夹内图片并分类）.py}进行验证，或者进行微调验证后标注直至数据集够大训练出满意的.pt模型。分类训练分为颜色分类和朝向分类两个模型<br>
4 --滑动验证码：<br><br>
    说明：在经历多次训练，识别后，YOLO11-obb{定向检测}和YOLO11-pose{姿势/关键点}已经YOLO11-seg{实例分割}都不尽人意，最终还是选择最基础的检测模型，识别区域只选突出部位可见图{8.jpg}，在训练是禁用水平和垂直旋转/或者也可以使用opencv进行灰度检测或边缘检测等，以下为yolo检测模型识别滑动验证码<br>
    文件库{.\YOLO训练\滑动训练},进行数据标注后修改{icon.yaml}为你的路径，后使用{maina .py}训练模型，后使用{视频测试识别.py}检测模型，直至模型能准确识别。<br>
7--使用opencv和CnOcr识别文件并对图片进行定向剪切<br><br>
    文件夹{.\图像处理}<br>
    {查找请点击位置.py}功能：识别文字，并查找return文字所在位置。<br>
    {图片处理.py}opencv对图像转换。<br>
    {图片查找所在图片的位置.py}根据一张小图，查找是否在另一种图中（实际使用中可以识别是否进入到验证码判断界面）。<br>
    {文字识别3.py}使用CnOcr来识别单行文字（请截取出单行文字后再识别确保识别准确率，在实际使用中可结合results = results.replace("xx", "yy")  # 把所有的 "xx" 替换成 "yy"）对识别的文件矫正。<br>
8--使用训练好的yolo模型来进行图片识别<br><br>
    说明：由于我将验证逻辑写入到一个py中并未进行太多成不同文件，所以以下两个.py会包含第9/10中的数据处理<br>
    图像验证：<br>
    文件：{./yzmmain.py}说明：21-36：对原图片进行预处理，只剪切需要识别的区域保证识别准确率。41-54：使用{3.形状识别}中训练的bast.pt模型进行对图像识别：<br>
    result = results[0]  # 直接获取单图结果<br>
    img_name = os.path.basename(img_path)<br>
    orig_img = result.orig_img  # 获取原始图像数据<br>
    # 保存标签文件<br>
    txt_path = os.path.join(save_dir, img_name.replace('.png', '.txt'))<br>
    result.save_txt(txt_path)，保存的识别文件在当前文件下run文件夹下，如果无需保存可修改   results = model.predict(<br>
        source=img_path,<br>
        conf=0.2,<br>
        save=True,<br>
        project=save_dir,<br>
        name='',<br>
        exist_ok=True<br>
    )中的True为Flase<br>
    102-132：对识别结果进行数据处理，写入到字典中，并对每一个模型使用crop_image函数进行剪切，再使用{识别颜色并分类.py}和{识别颜色并分类.py}中的函数获取剪切后图片文件夹中的朝向和颜色，<br>
    135-168：将拿到的形状，颜色，朝向，三个字典进行相互映射，获取包含此图片验证码所有信息的最终字典your_dict。<br>
    169-174：按照特定坐标和识别位置对验证码下方的文字区域进行剪切并识别文字。<br>
    175-181:将识别到的文字进行预处理，修正，剪切<br>
    182-310：根据文字对不同验证码的不同类别进行特定识别来找到不同情况的点击逻辑和点击位置需要用到的函数位于{查找字典中对应的序号的值.py}和{求重叠面积.py}中<br>
    310-final：对点击图片进行保存，标注点击位置便于后续验证。遍历文件夹内所有图片检查代码最终效果。<br>
    滑动验证：<br>
    文件：{./识别滑块验证.py}<br>
    说明：逻辑基于{求重叠面积.py}识别滑块A和缺口B的最大重叠面积找到AB坐标。<br>
9-对yolo识别的数据处理<br><br>
    在results = yolo(<br>
        source=tupian,<br>
        save=True,<br>
        conf=0.2,<br>
    )后，Yolo识别反正的值通常包含大量数据，可以通过正则表达式等对数据进行处理，找到位置：坐标：类别等，存入字典，在主函数中便于判断，可参考{查找字典中对应的序号的值.py}中函数。<br>
10-云端部署：<br><br>
    在完成1-9后我们已经完成了本地部署，但是在面临手机，低配模拟器，云手机等设备时无法使用本地调用，或者在有多台设备时需要在每一太设备上进行部署，非常麻烦。同时CnOcr文字识别等占用瞬时资源较大，需要高配cpu和显卡，为了应对这些文件我们可以采用云端部署，将部署好项目的电脑作为图片处理工作站，其余设备遇到验证码时上传图片，经工作站识别处理反正给识别数据和点击坐标来完成自动化过验证码，次方法可以完美解决跨设备使用问题。<br>
    部署逻辑可参考图{.\部署\验证流程.png}<br>
    需要设备：mysql数据库（纯粹图片状态，点击位置等）数据库格式（可参考）：<br>
    +--------------+--------------+------+-----+---------+-------+
| Field        | Type         | Null | Key | Default | Extra |
+--------------+--------------+------+-----+---------+-------+
| id           | varchar(255) | NO   | PRI | NULL    |       |
| cishuo       | int          | YES  |     | NULL    |       |
| keyongcishuo | int          | YES  |     | NULL    |       |
| zhuangtai    | int          | YES  |     | NULL    |       |
| remark       | varchar(255) | YES  |     | NULL    |       |
+--------------+--------------+------+-----+---------+-------+<br>
    一个flask框架来传输图片，服务器端:{server.py}本地设备端{服务器.py}<br>
    mysql：{数据库.py}<br>
    注意需要将以上代码中的接口和ip和端口地址修改为自己服务器的<br>
    本地工作站过验证码主程序：{主程序过验证码.py}说明：（通过不间断的循环来查找MySQL中代码验证码的一行是否为True，然后获取次行数据，设备id等，下载图片，本地识别，上传点击位置）<br>
    要设备的设备接口代码{过验证码发送.py}<br>
11-最后说明<br><br>
    自此已经完成了验证码从抓包获取数据，数据标注，训练模型，图片预处理，yolo识别图片，识别后的数据，本地部署，接入服务器完整一套流程。<br>
    次项目也可用于其余验证码项目，只需根据不同验证码训练不同的视觉模型和判断逻辑即可。或者BurtSuipe抓包伪造请求从实现无需点击从底层逻辑偏过服务商可见，经测试本项目部署的产品中和大多数都未进行加密处理，对比纯视觉算法实现难道要简易很多，当然被发现惩罚机制也严重很多。<br>
    最初版瑕疵较多，当然为了赶工文档也比较凌乱只挑选了重要地方和整体项目逻辑，项目中包含大量代码需自行理解或者gpt，为了方便理解将代码.py文件拆分到不同文件夹，在实际部署中需要将代码中的{文件名}{服务器ip}{端口号}{mysql账号密码}等修改为自己的，将需要调用的{.py}文件放到主函数目录下。如若有空会抽空完善此项目，即从0基础部署。<br>
