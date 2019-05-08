> 计64	嵇天颖	2016010308

### Cache 替换策略设计与分析

---

**目录**

[TOC]

---

#### 一、实验目的

1. 深入理解各种不同的 Cache 替换策略
2. 理解学习不同替换策略对程序运行性能的影响 
3. 动手实现自己的 Cache 替换策略



####  二、实验内容

1. 理解学习 LRU 及其它已经提出的 Cache 替换策略
2. 在提供的模拟器上实现⾃⼰设计的 Cache 替换策略
3. 通过 benchmark 测试⽐较不同的 Cache 替换策略
4. 在实验报告中简要说明不同 Cache 替换策略的核⼼思想和算法
5. 在实验报告中说明⾃⼰是怎样对不同的 Cache 替换策略进⾏测试的
6. 在实验报告中分析不同替换策略下，程序的运⾏时间、Cache 命中率受到的
影响



#### 三、不同Cache替换策略分析

##### 最佳置换（OPT）算法

* 理想置换算法）：从主存中移出永远不再需要的页面；如无这样的页面存在，则选择最长时间不需要访问的页面。于所选择的被淘汰页面将是以后永不使用的，或者是在最长时间内不再被访问的页面，这样可以保证获得最低的缺页率。 

* 优点：可以保证获得最低的缺页率。 
* 缺点：无法预测未来，故无法实现。



##### 随机（Random)算法

* 每次发生缺失时根据随机数选取一块替换即可。

* 优点：实现简单，运行速度快，对各种情况的访问都有一定的免疫力。

* 缺点：缺失率高，没有考虑到访问的特性，替换效率不稳定。

  

##### 最近最少使用（LRU）算法

* LRU算法通过过去的访问模式估计未来的访问模式，每次选择最长未被使用的被替换出去。
* 实现：增加标志位，每次将命中块之前的标志位增加，命中块标志位置0，缺失时选择标志位最大的块替换出去。
* 优点：在大部分情况下效果都比较好，当程序有较好的局部性，且cache容量足够大，LRU的命中率比较高。
* 缺点：随着路数的增加，需要增加额外的空间，算法引入的额外计算时间也逐渐增加。如果程序有类似扫描的访问模式，且扫描长度大于Cache容量，那么LRU算法的缺失率会比较高。



#####  最近最常使用算法（MRU）算法

* 这个缓存算法最先移除最近最常使用的条目。

* 优点：MRU算法擅长处理一个条目越久，越容易被访问的情况。

  

##### 先进先出（FIFO）算法

* 遵循先入先出原则，若当前Cache被填满，则替换最早进入Cache的那个。
* 优点：这个算法引入的额外计算量比LRU少。
* 缺点：受运行程序影响较大，可能会使得页面频繁刷新。



#####  时钟（CLOCK）算法

* LRU算法的性能接近于OPT,但是实现起来比较困难，且开销大；FIFO算法实现简单，但性能差。Clock算法是针对LRU遍历链表等开销较大的一种改进，将使用的列表改成环形链表，属于FIFO的复杂度。、

* 实现：替换方式

  ~~~c
  Hit：将reference bit设置为1
  
  Miss：从Head开始查找Reference bit为0 的entry
  
  如果Reference bit为1，清除该位，指针前移，直到找到为0的entry为止。
  
  如果Reference bit 为0， 将数据放入该entry，并将Reference bit置1。
  ~~~

* 优点：性能接近LRU算法，但开销要小



##### 自适应混合模型

* Ranjith Subramanian, Yannis Smaragdakisy和Gabriel H.Loh提出了一种Adaptive Caching 模型，可以混合任意两种Cache替代算法并且自适应的切换以贴近给定程序的局部特性的机制。
* 实现：增加了一些硬件结构，其中有两个Tag Array 是用来表示两种不同算法A和B下产生Cache内容，不含数据内容；另一个是失配历史缓存，用来反应对应的Cache Set的替换算法的性能。每当真实的Tag Array出现一次miss时，会检查这个历史缓存并模拟miss次数更少的替换算法。他们为了减少所需硬件，采用了Partial Tags。
* 优点：AC策略平均能提高了12%的CPI，只需要增加5%的Cache容量。相比较而言，使用其他增加路数的方式来获得相同的性能提升需要25%的Cache容量。



##### 依据工作集特性提出的（LIP,BIP,DIP）算法

* 背景：当程序重用Working Set大于可用Cache时或者其存储访问具有低局部相关性时，Cache替换策略中最常用的LRU策略表现出十分低下的命中率。大量新替换入Cache的行对命中率的贡献为零，而原本可能命中的行则由于长期不被访问而替换出Cache。

  如果Working Set的一些片段能被驻留于Cache中而不被LRU策略替换，将能有效地提高Cache的命中率。文章将Cache替换策略分为两个部分：牺牲者选择策略和插入策略，并通过简单地修改插入策略显著地改善Cache性能，且无需对现有硬件设计作大的改动或消耗大量的存储空间。

* Moinuddin K.Qureshi和Aamer Jaleel等依据工作集的特性，将Cache替换算法分为replace和insert两个部分，提出了LRU Insertion Policy(LIP),Bimodal Insertion Policy(BIP)算法，并在这两个算法的基础上提出了Dynamic Insertion Policy(DIP)算法。

* LRU Insertion Policy (LIP) ：该策略将所有替换入Cache的行置于LRU端。相对于传统策略将所有替换入的行置于MRU端，LIP使一部分行得以驻留于Cache中，其驻留时间能比Cache本身容量更长。LIP策略能够很好地应对Thrashing，尤其对于循环访问内存的程序其性能近似于OPT策略。由于LIP中并没有引入Age，其无法响应Working Set的切换。

* Bimodal Insertion Policy (BIP) 。BIP策略是对LIP的加强和改进，新换入的行会小概率地被置于MRU端。BIP可以很好地响应Working Set的切换，并保持一定的命中率。

* 以上两种策略对于LRU-friendly（高局部性）的程序，性能均不佳。

* Dynamic Insertion Policy (DIP) 能动态地在LRU和BIP间切换，选择其中命中率较高的策略执行后续指令。DIP对于LRU-friendly的程序块使用LRU策略，对于LRU-averse的程序块使用DIP策略，以求通用效率。对于1MB16路L2 Cache，DIP策略较LRU降低21%的失配率。

* 文中还提出了Set Dueling作为DIP中的调度选择策略。Set Dueling选择块中的少部分来分别执行两种竞争策略，而其余部分执行两者中失配率较低者。Set Dueling方法除了失配计数器，并不需要额外的Cache开销。



#### 四、实现的算法与实验结果

我在实验中实现了FIFO, CLOCK, LIP, BIP 算法：

~~~c
// Replacement Policies Supported
typedef enum 
{
    CRC_REPL_LRU        = 0,
    CRC_REPL_RANDOM     = 1,
    CRC_REPL_FIFO       = 2,
    CRC_REPL_CLOCK      = 3,
    CRC_REPL_LIP        = 4,
    CRC_REPL_BIP        = 5   
} ReplacemntPolicy;
~~~



实验结果如下：

**LRU算法**

| traces     | Instructions | CPI      | MissRate |
| ---------- | ------------ | -------- | -------- |
| perlbench  | 13796184     | 0.642823 | 40.7952  |
| bzip2      | 105737858    | 0.554642 | 61.7369  |
| gcc        | 111023833    | 0.614864 | 42.7521  |
| bwaves     | 100767249    | 0.253088 | 99.6634  |
| gamess     | 109857040    | 0.30022  | 26.3204  |
| mcf        | 111834055    | 2.55358  | 75.676   |
| milc       | 104433837    | 1.14939  | 77.0164  |
| zeusmp     | 103951560    | 0.451633 | 80.81    |
| gromacs    | 111463802    | 0.607769 | 71.1979  |
| cactusADM  | 113865457    | 0.44249  | 76.1164  |
| leslie3d   | 108598282    | 1.50626  | 84.0284  |
| namd       | 104034990    | 0.273795 | 66.2603  |
| gobmk      | 110811576    | 0.383876 | 14.919   |
| dealII     | 110728687    | 0.463916 | 45.0892  |
| soplex     | 60497953     | 0.356909 | 15.2011  |
| povray     | 113586629    | 0.360431 | 39.9258  |
| calculix   | 112031276    | 0.321346 | 34.05    |
| hmmer      | 110174490    | 0.258513 | 71.4736  |
| sjeng      | 110877774    | 0.323006 | 93.5415  |
| GemsFDTD   | 115939356    | 0.368143 | 84.1525  |
| libquantum | 116885396    | 0.272749 | 100      |
| h264ref    | 112187921    | 0.28787  | 70.0086  |
| tonto      | 100054260    | 0.347856 | 78.8694  |
| lbm        | 103428771    | 1.15379  | 99.9725  |
| omnetpp    | 117157993    | 0.41278  | 59.4443  |
| astar      | 108177102    | 0.267647 | 5.84718  |
| sphinx3    | 113061004    | 0.445644 | 97.156   |
| xalancbmk  | 116559218    | 0.414993 | 66.2759  |
| specrand   | 68635436     | 0.336211 | 95.9373  |





##### FIFO算法

| traces     | Instructions | CPI      | MissRate |
| ---------- | ------------ | -------- | -------- |
| perlbench  | 13796184     | 0.647953 | 41.6694  |
| bzip2      | 105737858    | 0.55759  | 62.1787  |
| gcc        | 111023833    | 0.631048 | 44.9167  |
| bwaves     | 100767249    | 0.253088 | 99.6634  |
| gamess     | 109857040    | 0.301266 | 26.7975  |
| mcf        | 111834055    | 2.6095   | 77.8556  |
| milc       | 104433837    | 1.14925  | 76.8283  |
| zeusmp     | 103951560    | 0.454532 | 82.5232  |
| gromacs    | 111463802    | 0.609378 | 71.4938  |
| cactusADM  | 113865457    | 0.451664 | 77.6336  |
| leslie3d   | 108598282    | 1.4964   | 83.0144  |
| namd       | 104034990    | 0.273795 | 66.2719  |
| gobmk      | 110811576    | 0.407287 | 21.1091  |
| dealII     | 110728687    | 0.46456  | 46.1974  |
| soplex     | 60497953     | 0.357608 | 15.3817  |
| povray     | 113586629    | 0.360529 | 40.2198  |
| calculix   | 112031276    | 0.323023 | 34.4734  |
| hmmer      | 110174490    | 0.258515 | 71.4999  |
| sjeng      | 110877774    | 0.323511 | 94.3372  |
| GemsFDTD   | 115939356    | 0.368143 | 84.1525  |
| libquantum | 116885396    | 0.272749 | 100      |
| h264ref    | 112187921    | 0.289111 | 70.4079  |
| tonto      | 100054260    | 0.348005 | 79.3838  |
| lbm        | 103428771    | 1.15428  | 99.9801  |
| omnetpp    | 117157993    | 0.412909 | 59.9028  |
| astar      | 108177102    | 0.267647 | 5.84718  |
| sphinx3    | 113061004    | 0.445673 | 97.315   |
| xalancbmk  | 116559218    | 0.417564 | 66.9845  |
| specrand   | 68635436     | 0.336209 | 95.8733  |

我们观察FIFO算法的表现，发现FIFO算法的CPI和MISSRATE受程序影响。在MISSRATE和CPI的平均表现上都没有CLOCK算法优良。这个FIFO算法其实比较暴力，其实也是LRU的思想，但可能就是线性化的、极度简单话的LRU。如果程序的局部性好的话，而且数据规模尚可，没有大量数据Thrashing这种操作的话，CPI和MISSRATE表现都挺好的。





##### CLOCK算法

| traces     | Instructions | CPI      | MissRate |
| ---------- | ------------ | -------- | -------- |
| perlbench  | 13796184     | 0.644415 | 41.1228  |
| bzip2      | 105737858    | 0.555128 | 62.1271  |
| gcc        | 111023833    | 0.621898 | 43.5188  |
| bwaves     | 100767249    | 0.253088 | 99.6634  |
| gamess     | 109857040    | 0.30083  | 26.5248  |
| mcf        | 111834055    | 2.58173  | 76.7433  |
| milc       | 104433837    | 1.14843  | 76.6981  |
| zeusmp     | 103951560    | 0.45283  | 81.4494  |
| gromacs    | 111463802    | 0.612216 | 71.7569  |
| cactusADM  | 113865457    | 0.450521 | 77.3741  |
| leslie3d   | 108598282    | 1.50466  | 83.9634  |
| namd       | 104034990    | 0.273795 | 66.2719  |
| gobmk      | 110811576    | 0.391202 | 17.1557  |
| dealII     | 110728687    | 0.467863 | 47.1231  |
| soplex     | 60497953     | 0.356944 | 15.246   |
| povray     | 113586629    | 0.360449 | 39.9801  |
| calculix   | 112031276    | 0.322505 | 34.1872  |
| hmmer      | 110174490    | 0.258513 | 71.4868  |
| sjeng      | 110877774    | 0.323332 | 94.0842  |
| GemsFDTD   | 115939356    | 0.368143 | 84.1525  |
| libquantum | 116885396    | 0.272749 | 100      |
| h264ref    | 112187921    | 0.28851  | 70.1737  |
| tonto      | 100054260    | 0.347968 | 79.2599  |
| lbm        | 103428771    | 1.15406  | 99.9772  |
| omnetpp    | 117157993    | 0.412819 | 59.5862  |
| astar      | 108177102    | 0.267647 | 5.84718  |
| sphinx3    | 113061004    | 0.445651 | 97.1913  |
| xalancbmk  | 116559218    | 0.416242 | 66.6189  |
| specrand   | 68635436     | 0.336209 | 95.8733  |

Clock算法是类似LRU选择Victim,它选择最早的最近使⽤较少的块替换出。Clock算法是LRU与FIFO算法的综合，命中率接近LRU算法。CLOCK算法缺失率的性能表现比较好，而且时间代价并不是很高。

Clock是环形列表结构，并且标志位的存在使得每次Update时效率要比LRU高，因此CPI较之LRU更短一些。



##### LIP算法

| traces     | Instructions | CPI      | MissRate |
| ---------- | ------------ | -------- | -------- |
| perlbench  | 13796184     | 0.669326 | 44.9668  |
| bzip2      | 105737858    | 0.571873 | 55.3261  |
| gcc        | 111023833    | 0.575939 | 38.5965  |
| bwaves     | 100767249    | 0.253088 | 99.6634  |
| gamess     | 109857040    | 0.312251 | 92.0923  |
| mcf        | 111834055    | 2.04087  | 59.7033  |
| milc       | 104433837    | 1.1807   | 79.3471  |
| zeusmp     | 103951560    | 0.452046 | 82.492   |
| gromacs    | 111463802    | 0.664129 | 89.1534  |
| cactusADM  | 113865457    | 0.378492 | 63.7024  |
| leslie3d   | 108598282    | 1.4344   | 79.7774  |
| namd       | 104034990    | 0.273797 | 66.2661  |
| gobmk      | 110811576    | 0.388093 | 15.5215  |
| dealII     | 110728687    | 0.446134 | 47.2678  |
| soplex     | 60497953     | 0.431378 | 35.9993  |
| povray     | 113586629    | 0.360387 | 39.7901  |
| calculix   | 112031276    | 0.359601 | 53.1214  |
| hmmer      | 110174490    | 0.258513 | 71.4868  |
| sjeng      | 110877774    | 0.322841 | 93.3249  |
| GemsFDTD   | 115939356    | 0.368143 | 84.1525  |
| libquantum | 116885396    | 0.272749 | 100      |
| h264ref    | 112187921    | 0.292871 | 72.4714  |
| tonto      | 100054260    | 0.34803  | 79.2837  |
| lbm        | 103428771    | 1.15439  | 99.7331  |
| omnetpp    | 117157993    | 0.412729 | 59.2859  |
| astar      | 108177102    | 0.267647 | 5.84718  |
| sphinx3    | 113061004    | 0.445645 | 97.1648  |
| xalancbmk  | 116559218    | 0.411322 | 63.1589  |
| specrand   | 68635436     | 0.336348 | 97.6647  |

LIP策略能够很好地应对Thrashing，这有利地缓解了LRU那一系列的算法在Trashing下的缺陷。在大部分Trace中LIP算法的缺失率表现都比CLOCK好，但是在gromacs和soplex这两个程序中表现极为不佳，LIP的CPI表现比CLOCK优越很多。





##### 图表汇总

我们将部分实验结果汇总成图表，以便直观的进行分析：

首先是不同算法的CPI值，我们可以发现LRU系列算法（FIFO,CLOCK,LRU)基本上CPI持平，而区分了insert和replace操作的LIP的运算速度会优于他们。

![1556984857143](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\1556984857143.png)



其次是不同算法的MissRate比较：

![1556985098700](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\1556985098700.png)

我们发现LIP算法并没有很明显的改进LRU算法，大约三分之一的情况下LIP算法表现更好，但是有一半的情况下LRU表现更好。因为LRU优良的稳定性，和较好的MISSRATE的表现，我在跑BIP程序的时候，尽量把选择LRU的概率稍微设置的大一些，我设置成了35%。通常来说，程序的局部性更强时LRU算法表现会比较好，当程序的局部性表现有较大波动时，LIP一类改进算法会表现更好。实际上看论文知道，DIP算法的动态调节表现应该是最好的，不过本次实验来不及进行实现了。





#### 五、实验心得

此次实验让我对Cache算法有了更深刻的理解，在实验中，尤其是跑数据的时候，让我很直观的感受到不同算法的不同性质。通过阅读一些资料和论文，我也了解了不少课堂上没有学过的新的Cache算法（虽然没有实现），感受了Cache领域的发展，收获颇多。

PS：这次实验在欢乐的五一假期中写着，在家真的是这儿玩耍那儿玩耍，懒惰的我就写个脚本，让电脑自个儿跑trace，把数据自己导出成excel，然后去愉快玩耍。到最后发现自己这么不虚原来是记错了DDL，4号晚上开始疯狂写报告，本来心心念念着想试一试DIP也来不及了。
