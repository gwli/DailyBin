 CREATE TABLE `chat_logs` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `content` varchar(255) DEFAULT NULL COMMENT '聊天内容',
  `group_number` varchar(255) DEFAULT NULL,
  `group_name` varchar(255) DEFAULT NULL,
  `qq` varchar(255) DEFAULT NULL,
  `nickname` varchar(255) DEFAULT NULL,
  `mark` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=5093 DEFAULT CHARSET=utf8 COMMENT='聊天记录表';

create trigger `delete_empty` after insert on `chat_logs`
for each row
    DELETE FROM chat_logs where (content='');

select content,group_name,nickname from chat_logs where date(create_time) = curdate() order by group_number,qq; 
