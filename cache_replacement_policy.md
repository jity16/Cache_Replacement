FIFO

CLOCK

传统的FIFO和LRU算法都没有使用访问次数这个信息，使得对于空间局限性较弱的场景效率很低，Second Change算法对FIFO算法做了略微的修改，在一定程度上可以改善这种场景下的效率。该算法依然使用队列的方式访问，同时为队列的每一项设置一个参考位。

Clock算法是针对LRU遍历链表等开销较大的一种改进，将Second Change使用的列表改成环形链表，属于FIFO的复杂度。Clock 不需要从Front移除数据到Rear端，使用Head指针替代了Front和Rear指针。

替换方式和Second Change相似：

Hit：将reference bit设置为1

Miss：从Head开始查找Reference bit为0 的entry

如果Reference bit为1，清除该位，指针前移，直到找到为0的entry为止。

如果Reference bit 为0， 将数据放入该entry，并将Reference bit置1。



简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。