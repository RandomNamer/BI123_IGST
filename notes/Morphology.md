<h2 style="border: none;">Morphology</h2>

### Mathematical morphology in gray scale (3)

#### Conditional Dilation

aka *Morphological Reconstruction*

将膨胀结果与mask求and，有针对性地提取mask的部分。

**Graysale：** Opening/Closing，之后reconstruct

#### Watershed

**测地线距离(Geodesic Distance)**：测地线距离就是地球表面两点之间的最短路径（可执行路径）的距离，在图论中，Geodesic Distance 就是图中两节点的最短路径的距离，这与平时在几何空间通常用到的 Euclidean Distance（欧氏距离），即两点之间的最短距离有所区别。

<img src="/Users/zzy/Library/Application Support/typora-user-images/image-20211123111319160.png" alt="image-20211123111319160" style="zoom:33%;" />

**Watershed：**

1. 把梯度图像中的所有像素按照灰度值进行分类，并设定一个测地距离阈值。
2. 找到灰度值最小的像素点（默认标记为灰度值最低点），让threshold从最小值开始增长，这些点为起始点。
3. 水平面在增长的过程中，会碰到周围的邻域像素，测量这些像素到起始点（灰度值最低点）的测地距离，如果小于设定阈值，则将这些像素淹没，否则在这些像素上设置大坝，这样就对这些邻域像素进行了分类。
4. 直到灰度值的最大值，所有区域都在分水岭线上相遇，这些大坝就对整个图像像素的进行了分区。

https://zhuanlan.zhihu.com/p/67741538

