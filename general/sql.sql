CREATE DATABASE IF NOT EXISTS datapro;

USE datapro;
# visit = 1表示该链接已经被访问.
# 基本上所有的表的结构都是相似的.


CREATE TABLE IF NOT EXISTS yimai_link(
  id INT PRIMARY KEY AUTO_INCREMENT,
  link VARCHAR(3000),
  visit INT
);

# 保存阿里研究院链接
CREATE TABLE IF NOT EXISTS ali_link(
  id INT PRIMARY KEY AUTO_INCREMENT,
  link VARCHAR(3000),
  visit INT
);

# 保存麦肯锡链接
CREATE TABLE mkx_link(
  id INT PRIMARY KEY AUTO_INCREMENT,
  link VARCHAR(3000),
  visit INT
);