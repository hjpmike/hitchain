/*
Navicat MySQL Data Transfer

Source Server         : 110
Source Server Version : 50553
Source Host           : 10.107.10.110:3306
Source Database       : lyz

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2018-07-19 11:41:04
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for twitters_data
-- ----------------------------
DROP TABLE IF EXISTS `twitters_data`;
CREATE TABLE `twitters_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coin_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `tweets_num` int(11) DEFAULT NULL,
  `followers_num` int(11) DEFAULT NULL,
  `following_num` int(11) DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=266 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of twitters_data
-- ----------------------------
INSERT INTO `twitters_data` VALUES ('1', '1', 'Bitcoin', '20685', '871791', '189', '2018-07-17 22:17:41');
INSERT INTO `twitters_data` VALUES ('2', '2', 'Ethereum', '1913', '2211', '409009', '2018-07-17 22:18:00');
INSERT INTO `twitters_data` VALUES ('3', '3', 'XRP', '6128', '879426', '749', '2018-07-17 22:18:20');
INSERT INTO `twitters_data` VALUES ('4', '4', 'Bitcoin Cash', '1014', '105020', '38', '2018-07-17 22:18:26');
INSERT INTO `twitters_data` VALUES ('5', '5', 'EOS', '995', '179973', '47', '2018-07-17 22:18:32');
INSERT INTO `twitters_data` VALUES ('6', '6', 'Litecoin', '136', '3', '31197', '2018-07-17 22:18:41');
INSERT INTO `twitters_data` VALUES ('7', '7', 'Stellar', '2510', '242841', '1540', '2018-07-17 22:18:51');
INSERT INTO `twitters_data` VALUES ('8', '8', 'Cardano', '1428', '142166', '502', '2018-07-17 22:18:57');
INSERT INTO `twitters_data` VALUES ('9', '9', 'IOTA', '725', '23', '114673', '2018-07-17 22:19:02');
INSERT INTO `twitters_data` VALUES ('10', '10', 'Tether', '272', '26286', '383', '2018-07-17 22:19:09');
INSERT INTO `twitters_data` VALUES ('11', '11', 'TRON', '1046', '316882', '163', '2018-07-17 22:19:16');
INSERT INTO `twitters_data` VALUES ('12', '12', 'NEO', '612', '662', '317316', '2018-07-17 22:19:22');
INSERT INTO `twitters_data` VALUES ('13', '13', 'Monero', '2852', '301747', '12', '2018-07-17 22:19:26');
INSERT INTO `twitters_data` VALUES ('14', '14', 'Dash', '2877', '308438', '288', '2018-07-17 22:19:30');
INSERT INTO `twitters_data` VALUES ('15', '15', 'Ethereum Classic', '3305', '208780', '541', '2018-07-17 22:19:42');
INSERT INTO `twitters_data` VALUES ('16', '17', 'Binance Coin', '2395', '305607', '810', '2018-07-17 22:20:31');
INSERT INTO `twitters_data` VALUES ('17', '18', 'VeChain', '377', '95499', '54', '2018-07-17 22:20:51');
INSERT INTO `twitters_data` VALUES ('18', '19', 'Tezos', '1', '250', '3', '2018-07-17 22:21:10');
INSERT INTO `twitters_data` VALUES ('19', '20', 'OmiseGO', '636', '283553', '1522', '2018-07-17 22:21:32');
INSERT INTO `twitters_data` VALUES ('20', '21', 'Qtum', '1078', '169654', '736', '2018-07-17 22:21:52');
INSERT INTO `twitters_data` VALUES ('21', '22', 'Zcash', '1483', '1167', '69496', '2018-07-17 22:22:13');
INSERT INTO `twitters_data` VALUES ('22', '23', 'Ontology', '1351', '58322', '212', '2018-07-17 22:22:33');
INSERT INTO `twitters_data` VALUES ('23', '24', 'Lisk', '1748', '185998', '335', '2018-07-17 22:22:53');
INSERT INTO `twitters_data` VALUES ('24', '25', 'Bytecoin', '2261', '43942', '764', '2018-07-17 22:23:17');
INSERT INTO `twitters_data` VALUES ('25', '26', 'ICON', '362', '108646', '11', '2018-07-17 22:23:36');
INSERT INTO `twitters_data` VALUES ('26', '27', 'Zilliqa ', '641', '47554', '73', '2018-07-17 22:23:54');
INSERT INTO `twitters_data` VALUES ('27', '29', '0x', '522', '130895', '53', '2018-07-17 22:24:37');
INSERT INTO `twitters_data` VALUES ('28', '30', 'Decred', '1306', '2605', '39350', '2018-07-17 22:24:51');
INSERT INTO `twitters_data` VALUES ('29', '31', 'BitShares', '1993', '89151', '2063', '2018-07-17 22:24:57');
INSERT INTO `twitters_data` VALUES ('30', '32', 'DigiByte', '4268', '146072', '446', '2018-07-17 22:25:03');
INSERT INTO `twitters_data` VALUES ('39', '33', 'Aeternity', '1', '781', '0', '2018-07-18 14:56:34');
INSERT INTO `twitters_data` VALUES ('40', '34', 'Maker', '362', '11818', '248', '2018-07-18 14:56:54');
INSERT INTO `twitters_data` VALUES ('41', '35', 'Siacoin', '957', '107030', '1465', '2018-07-18 14:57:06');
INSERT INTO `twitters_data` VALUES ('42', '36', 'Steem', '14504', '103412', '12977', '2018-07-18 14:57:09');
INSERT INTO `twitters_data` VALUES ('43', '37', 'Augur', '1889', '116536', '263', '2018-07-18 14:57:13');
INSERT INTO `twitters_data` VALUES ('44', '38', 'Verge ', '2396', '305589', '810', '2018-07-18 14:57:33');
INSERT INTO `twitters_data` VALUES ('45', '39', 'Nano', '345', '97151', '78', '2018-07-18 14:57:38');
INSERT INTO `twitters_data` VALUES ('46', '40', 'Bytom', '803', '18665', '238', '2018-07-18 14:57:42');
INSERT INTO `twitters_data` VALUES ('47', '41', 'Bitcoin Diamond', '609', '19882', '307', '2018-07-18 14:57:46');
INSERT INTO `twitters_data` VALUES ('48', '42', 'KuCoin Shares', '4200', '296838', '113', '2018-07-18 14:57:49');
INSERT INTO `twitters_data` VALUES ('49', '33', 'Aeternity', '1', '781', '0', '2018-07-18 15:10:17');
INSERT INTO `twitters_data` VALUES ('50', '34', 'Maker', '362', '11819', '248', '2018-07-18 15:10:36');
INSERT INTO `twitters_data` VALUES ('51', '35', 'Siacoin', '957', '107028', '1465', '2018-07-18 15:10:54');
INSERT INTO `twitters_data` VALUES ('52', '36', 'Steem', '14504', '103410', '12977', '2018-07-18 15:11:15');
INSERT INTO `twitters_data` VALUES ('53', '37', 'Augur', '1889', '116537', '263', '2018-07-18 15:11:27');
INSERT INTO `twitters_data` VALUES ('54', '38', 'Verge ', '2396', '305587', '810', '2018-07-18 15:11:48');
INSERT INTO `twitters_data` VALUES ('55', '39', 'Nano', '345', '97150', '78', '2018-07-18 15:11:52');
INSERT INTO `twitters_data` VALUES ('56', '40', 'Bytom', '803', '18666', '238', '2018-07-18 15:11:55');
INSERT INTO `twitters_data` VALUES ('57', '41', 'Bitcoin Diamond', '609', '19882', '307', '2018-07-18 15:12:02');
INSERT INTO `twitters_data` VALUES ('58', '42', 'KuCoin Shares', '4201', '296838', '113', '2018-07-18 15:12:05');
INSERT INTO `twitters_data` VALUES ('59', '33', 'Aeternity', '1', '781', '0', '2018-07-18 15:35:43');
INSERT INTO `twitters_data` VALUES ('60', '34', 'Maker', '362', '11819', '248', '2018-07-18 15:35:46');
INSERT INTO `twitters_data` VALUES ('61', '35', 'Siacoin', '957', '107030', '1465', '2018-07-18 15:35:50');
INSERT INTO `twitters_data` VALUES ('62', '36', 'Steem', '14504', '103414', '12977', '2018-07-18 15:35:54');
INSERT INTO `twitters_data` VALUES ('63', '37', 'Augur', '1889', '116539', '263', '2018-07-18 15:35:58');
INSERT INTO `twitters_data` VALUES ('64', '38', 'Verge ', '2396', '305588', '810', '2018-07-18 15:36:18');
INSERT INTO `twitters_data` VALUES ('65', '39', 'Nano', '345', '97148', '78', '2018-07-18 15:36:22');
INSERT INTO `twitters_data` VALUES ('66', '40', 'Bytom', '803', '18673', '238', '2018-07-18 15:36:25');
INSERT INTO `twitters_data` VALUES ('67', '41', 'Bitcoin Diamond', '609', '19881', '307', '2018-07-18 15:36:29');
INSERT INTO `twitters_data` VALUES ('68', '42', 'KuCoin Shares', '4201', '296843', '113', '2018-07-18 15:36:32');
INSERT INTO `twitters_data` VALUES ('69', '43', 'Waltonchain', '0', '0', '0', '2018-07-18 15:36:34');
INSERT INTO `twitters_data` VALUES ('70', '44', 'Pundi X', '1066', '33970', '156', '2018-07-18 15:36:39');
INSERT INTO `twitters_data` VALUES ('71', '45', 'Dogecoin', '417', '121830', '9', '2018-07-18 15:36:44');
INSERT INTO `twitters_data` VALUES ('72', '47', 'Waves ', '2710', '130565', '2', '2018-07-18 15:36:48');
INSERT INTO `twitters_data` VALUES ('73', '50', 'Populous ', '587', '23685', '37', '2018-07-18 15:36:52');
INSERT INTO `twitters_data` VALUES ('74', '51', 'Stratis ', '0', '0', '0', '2018-07-18 15:37:10');
INSERT INTO `twitters_data` VALUES ('75', '52', 'Status', '1266', '105067', '441', '2018-07-18 15:37:14');
INSERT INTO `twitters_data` VALUES ('76', '53', 'Wanchain', '202', '109392', '76', '2018-07-18 15:37:17');
INSERT INTO `twitters_data` VALUES ('77', '54', 'Hshare', '494', '12270', '55', '2018-07-18 15:37:23');
INSERT INTO `twitters_data` VALUES ('78', '55', 'DigixDAO', '472', '15602', '541', '2018-07-18 15:37:27');
INSERT INTO `twitters_data` VALUES ('79', '56', 'Mithril ', '344', '17616', '134', '2018-07-18 15:37:30');
INSERT INTO `twitters_data` VALUES ('80', '58', 'Mixin ', '99', '10', '3283', '2018-07-18 15:37:33');
INSERT INTO `twitters_data` VALUES ('81', '59', 'Bitcoin Private', '400', '105', '52037', '2018-07-18 15:37:37');
INSERT INTO `twitters_data` VALUES ('82', '60', 'Komodo', '2891', '91359', '87', '2018-07-18 15:37:40');
INSERT INTO `twitters_data` VALUES ('83', '61', 'Aion', '955', '52334', '1454', '2018-07-18 15:37:45');
INSERT INTO `twitters_data` VALUES ('84', '62', 'Huobi Token ', '2686', '72679', '335', '2018-07-18 15:37:49');
INSERT INTO `twitters_data` VALUES ('85', '63', 'MaidSafeCoin ', '3515', '57964', '337', '2018-07-18 15:37:52');
INSERT INTO `twitters_data` VALUES ('86', '64', 'GXChain', '650', '11147', '316', '2018-07-18 15:37:57');
INSERT INTO `twitters_data` VALUES ('87', '65', 'Nebulas ', '488', '23888', '41', '2018-07-18 15:38:01');
INSERT INTO `twitters_data` VALUES ('88', '66', 'Ardor', '0', '0', '0', '2018-07-18 15:38:05');
INSERT INTO `twitters_data` VALUES ('89', '67', 'Loopring', '1595', '28173', '362', '2018-07-18 15:38:09');
INSERT INTO `twitters_data` VALUES ('90', '68', 'Aelf', '410', '23545', '101', '2018-07-18 15:38:13');
INSERT INTO `twitters_data` VALUES ('91', '69', 'Ark', '1308', '64459', '2687', '2018-07-18 15:38:16');
INSERT INTO `twitters_data` VALUES ('92', '70', 'MonaCoin', '0', '0', '0', '2018-07-18 15:38:36');
INSERT INTO `twitters_data` VALUES ('93', '71', 'ReddCoin', '7698', '72897', '223', '2018-07-18 15:38:50');
INSERT INTO `twitters_data` VALUES ('94', '72', 'FunFair ', '545', '37099', '320', '2018-07-18 15:38:56');
INSERT INTO `twitters_data` VALUES ('95', '73', 'Kyber Network', '1227', '87472', '551', '2018-07-18 15:39:04');
INSERT INTO `twitters_data` VALUES ('96', '74', 'Loom Network', '750', '13430', '67', '2018-07-18 15:39:12');
INSERT INTO `twitters_data` VALUES ('97', '75', 'Emercoin', '157', '3370', '10', '2018-07-18 15:39:27');
INSERT INTO `twitters_data` VALUES ('98', '76', 'Dentacoin', '871', '18019', '487', '2018-07-18 15:39:31');
INSERT INTO `twitters_data` VALUES ('99', '77', 'MCO', '470', '65781', '58', '2018-07-18 15:39:34');
INSERT INTO `twitters_data` VALUES ('100', '78', 'WAX', '1595', '16981', '211', '2018-07-18 15:39:39');
INSERT INTO `twitters_data` VALUES ('101', '79', 'Gas', '1511', '452114', '1904', '2018-07-18 15:39:55');
INSERT INTO `twitters_data` VALUES ('102', '81', 'Bancor ', '1560', '73195', '102', '2018-07-18 15:40:07');
INSERT INTO `twitters_data` VALUES ('103', '82', 'Cryptonex', '220', '31120', '17', '2018-07-18 15:40:10');
INSERT INTO `twitters_data` VALUES ('104', '83', 'Veritaseum', '14972', '23197', '596', '2018-07-18 15:40:13');
INSERT INTO `twitters_data` VALUES ('105', '85', 'CyberMiles', '426', '297344', '139', '2018-07-18 15:40:17');
INSERT INTO `twitters_data` VALUES ('106', '86', 'Power Ledger', '3497', '86416', '2967', '2018-07-18 15:40:21');
INSERT INTO `twitters_data` VALUES ('107', '87', 'Ethos', '590', '60962', '991', '2018-07-18 15:40:34');
INSERT INTO `twitters_data` VALUES ('108', '88', 'MOAC', '255', '450', '741', '2018-07-18 15:40:37');
INSERT INTO `twitters_data` VALUES ('109', '89', 'PIVX', '2478', '60267', '396', '2018-07-18 15:40:41');
INSERT INTO `twitters_data` VALUES ('110', '90', 'Decentraland', '573', '37406', '176', '2018-07-18 15:40:44');
INSERT INTO `twitters_data` VALUES ('111', '91', 'Dropil', '133', '6964', '86', '2018-07-18 15:40:48');
INSERT INTO `twitters_data` VALUES ('112', '92', 'Paypex', '112', '2106', '903', '2018-07-18 15:40:51');
INSERT INTO `twitters_data` VALUES ('113', '93', 'QASH', '1508', '21711', '730', '2018-07-18 15:41:04');
INSERT INTO `twitters_data` VALUES ('114', '94', 'Polymath', '907', '28092', '167', '2018-07-18 15:41:07');
INSERT INTO `twitters_data` VALUES ('115', '95', 'ZenCash', '3101', '22154', '1403', '2018-07-18 15:41:11');
INSERT INTO `twitters_data` VALUES ('116', '96', 'Cortex', '153', '11087', '85', '2018-07-18 15:41:14');
INSERT INTO `twitters_data` VALUES ('117', '97', 'Noah Coin', '193', '67', '6443', '2018-07-18 15:41:18');
INSERT INTO `twitters_data` VALUES ('118', '98', 'Factom ', '2161', '77524', '486', '2018-07-18 15:41:22');
INSERT INTO `twitters_data` VALUES ('119', '99', 'Theta Token', '313', '54209', '143', '2018-07-18 15:41:34');
INSERT INTO `twitters_data` VALUES ('120', '100', 'Elastos', '382', '25486', '20', '2018-07-18 15:41:54');
INSERT INTO `twitters_data` VALUES ('121', '33', 'Aeternity', '1', '781', '0', '2018-07-18 15:43:41');
INSERT INTO `twitters_data` VALUES ('122', '34', 'Maker', '362', '11820', '248', '2018-07-18 15:44:01');
INSERT INTO `twitters_data` VALUES ('123', '35', 'Siacoin', '957', '107029', '1465', '2018-07-18 15:44:20');
INSERT INTO `twitters_data` VALUES ('124', '36', 'Steem', '14504', '103415', '12977', '2018-07-18 15:44:37');
INSERT INTO `twitters_data` VALUES ('125', '37', 'Augur', '1889', '116535', '263', '2018-07-18 15:44:55');
INSERT INTO `twitters_data` VALUES ('126', '33', 'Aeternity', '1', '781', '0', '2018-07-18 15:47:20');
INSERT INTO `twitters_data` VALUES ('127', '34', 'Maker', '362', '11820', '248', '2018-07-18 15:47:39');
INSERT INTO `twitters_data` VALUES ('128', '35', 'Siacoin', '957', '107029', '1465', '2018-07-18 15:47:58');
INSERT INTO `twitters_data` VALUES ('129', '36', 'Steem', '14504', '103415', '12977', '2018-07-18 15:48:15');
INSERT INTO `twitters_data` VALUES ('130', '33', 'Aeternity', '1', '781', '0', '2018-07-18 15:48:44');
INSERT INTO `twitters_data` VALUES ('131', '34', 'Maker', '362', '11820', '248', '2018-07-18 15:49:02');
INSERT INTO `twitters_data` VALUES ('132', '35', 'Siacoin', '957', '107029', '1465', '2018-07-18 15:49:21');
INSERT INTO `twitters_data` VALUES ('133', '36', 'Steem', '14504', '103415', '12977', '2018-07-18 15:49:38');
INSERT INTO `twitters_data` VALUES ('134', '37', 'Augur', '1889', '116535', '263', '2018-07-18 15:49:54');
INSERT INTO `twitters_data` VALUES ('135', '33', 'Aeternity', '1', '781', '0', '2018-07-18 15:50:46');
INSERT INTO `twitters_data` VALUES ('136', '34', 'Maker', '362', '11820', '248', '2018-07-18 15:51:26');
INSERT INTO `twitters_data` VALUES ('137', '33', 'Aeternity', '1', '781', '0', '2018-07-18 15:52:56');
INSERT INTO `twitters_data` VALUES ('138', '34', 'Maker', '362', '11820', '248', '2018-07-18 15:53:16');
INSERT INTO `twitters_data` VALUES ('139', '33', 'Aeternity', '1', '781', '0', '2018-07-18 15:53:40');
INSERT INTO `twitters_data` VALUES ('140', '34', 'Maker', '362', '11820', '248', '2018-07-18 15:53:59');
INSERT INTO `twitters_data` VALUES ('141', '35', 'Siacoin', '957', '107029', '1465', '2018-07-18 15:54:19');
INSERT INTO `twitters_data` VALUES ('142', '36', 'Steem', '14504', '103415', '12977', '2018-07-18 15:54:36');
INSERT INTO `twitters_data` VALUES ('143', '37', 'Augur', '1889', '116535', '263', '2018-07-18 15:54:56');
INSERT INTO `twitters_data` VALUES ('144', '38', 'Verge ', '2396', '305591', '810', '2018-07-18 15:55:36');
INSERT INTO `twitters_data` VALUES ('145', '33', 'Aeternity', '1', '781', '0', '2018-07-18 15:55:40');
INSERT INTO `twitters_data` VALUES ('146', '39', 'Nano', '345', '97149', '78', '2018-07-18 15:55:58');
INSERT INTO `twitters_data` VALUES ('147', '34', 'Maker', '362', '11820', '248', '2018-07-18 15:56:00');
INSERT INTO `twitters_data` VALUES ('148', '40', 'Bytom', '803', '18672', '238', '2018-07-18 15:56:20');
INSERT INTO `twitters_data` VALUES ('149', '35', 'Siacoin', '957', '107029', '1465', '2018-07-18 15:56:21');
INSERT INTO `twitters_data` VALUES ('150', '36', 'Steem', '14504', '103415', '12977', '2018-07-18 15:56:41');
INSERT INTO `twitters_data` VALUES ('151', '41', 'Bitcoin Diamond', '609', '19881', '307', '2018-07-18 15:56:45');
INSERT INTO `twitters_data` VALUES ('152', '33', 'Aeternity', '1', '781', '0', '2018-07-18 15:57:01');
INSERT INTO `twitters_data` VALUES ('153', '34', 'Maker', '362', '11820', '248', '2018-07-18 15:57:28');
INSERT INTO `twitters_data` VALUES ('154', '33', 'Aeternity', '1', '781', '0', '2018-07-18 15:58:18');
INSERT INTO `twitters_data` VALUES ('155', '34', 'Maker', '362', '11820', '248', '2018-07-18 15:58:37');
INSERT INTO `twitters_data` VALUES ('156', '35', 'Siacoin', '957', '107028', '1465', '2018-07-18 15:59:00');
INSERT INTO `twitters_data` VALUES ('157', '33', 'Aeternity', '1', '781', '0', '2018-07-18 16:00:43');
INSERT INTO `twitters_data` VALUES ('158', '34', 'Maker', '362', '11820', '248', '2018-07-18 16:01:03');
INSERT INTO `twitters_data` VALUES ('159', '35', 'Siacoin', '957', '107028', '1465', '2018-07-18 16:01:22');
INSERT INTO `twitters_data` VALUES ('160', '36', 'Steem', '14504', '103415', '12977', '2018-07-18 16:01:39');
INSERT INTO `twitters_data` VALUES ('161', '37', 'Augur', '1889', '116535', '263', '2018-07-18 16:01:58');
INSERT INTO `twitters_data` VALUES ('162', '38', 'Verge ', '2396', '305592', '810', '2018-07-18 16:02:47');
INSERT INTO `twitters_data` VALUES ('163', '39', 'Nano', '345', '97148', '78', '2018-07-18 16:02:59');
INSERT INTO `twitters_data` VALUES ('164', '33', 'Aeternity', '1', '781', '0', '2018-07-18 16:03:18');
INSERT INTO `twitters_data` VALUES ('165', '40', 'Bytom', '803', '18672', '238', '2018-07-18 16:03:19');
INSERT INTO `twitters_data` VALUES ('166', '34', 'Maker', '362', '11820', '248', '2018-07-18 16:03:45');
INSERT INTO `twitters_data` VALUES ('167', '35', 'Siacoin', '957', '107028', '1465', '2018-07-18 16:04:07');
INSERT INTO `twitters_data` VALUES ('168', '36', 'Steem', '14504', '103415', '12977', '2018-07-18 16:04:43');
INSERT INTO `twitters_data` VALUES ('169', '41', 'Bitcoin Diamond', '609', '19882', '307', '2018-07-18 16:04:43');
INSERT INTO `twitters_data` VALUES ('170', '42', 'KuCoin Shares', '4202', '296849', '113', '2018-07-18 16:04:58');
INSERT INTO `twitters_data` VALUES ('171', '37', 'Augur', '1889', '116536', '263', '2018-07-18 16:04:59');
INSERT INTO `twitters_data` VALUES ('172', '43', 'Waltonchain', '0', '0', '0', '2018-07-18 16:05:11');
INSERT INTO `twitters_data` VALUES ('173', '44', 'Pundi X', '1066', '33974', '156', '2018-07-18 16:05:16');
INSERT INTO `twitters_data` VALUES ('174', '38', 'Verge ', '2396', '305592', '810', '2018-07-18 16:05:30');
INSERT INTO `twitters_data` VALUES ('175', '39', 'Nano', '345', '97148', '78', '2018-07-18 16:05:37');
INSERT INTO `twitters_data` VALUES ('176', '40', 'Bytom', '803', '18672', '238', '2018-07-18 16:05:43');
INSERT INTO `twitters_data` VALUES ('177', '45', 'Dogecoin', '417', '121838', '9', '2018-07-18 16:05:47');
INSERT INTO `twitters_data` VALUES ('178', '41', 'Bitcoin Diamond', '609', '19882', '307', '2018-07-18 16:05:48');
INSERT INTO `twitters_data` VALUES ('179', '42', 'KuCoin Shares', '4202', '296849', '113', '2018-07-18 16:05:51');
INSERT INTO `twitters_data` VALUES ('180', '43', 'Waltonchain', '0', '0', '0', '2018-07-18 16:05:53');
INSERT INTO `twitters_data` VALUES ('181', '47', 'Waves ', '2710', '130559', '2', '2018-07-18 16:05:55');
INSERT INTO `twitters_data` VALUES ('182', '50', 'Populous ', '587', '23685', '37', '2018-07-18 16:05:59');
INSERT INTO `twitters_data` VALUES ('183', '44', 'Pundi X', '1066', '33974', '156', '2018-07-18 16:05:59');
INSERT INTO `twitters_data` VALUES ('184', '45', 'Dogecoin', '417', '121838', '9', '2018-07-18 16:06:02');
INSERT INTO `twitters_data` VALUES ('185', '47', 'Waves ', '2710', '130559', '2', '2018-07-18 16:06:06');
INSERT INTO `twitters_data` VALUES ('186', '50', 'Populous ', '587', '23685', '37', '2018-07-18 16:06:10');
INSERT INTO `twitters_data` VALUES ('187', '51', 'Stratis ', '0', '0', '0', '2018-07-18 16:06:16');
INSERT INTO `twitters_data` VALUES ('188', '52', 'Status', '1266', '105069', '441', '2018-07-18 16:06:23');
INSERT INTO `twitters_data` VALUES ('189', '53', 'Wanchain', '202', '109397', '76', '2018-07-18 16:06:26');
INSERT INTO `twitters_data` VALUES ('190', '51', 'Stratis ', '0', '0', '0', '2018-07-18 16:06:27');
INSERT INTO `twitters_data` VALUES ('191', '54', 'Hshare', '494', '12270', '55', '2018-07-18 16:06:29');
INSERT INTO `twitters_data` VALUES ('192', '52', 'Status', '1266', '105069', '441', '2018-07-18 16:06:30');
INSERT INTO `twitters_data` VALUES ('193', '55', 'DigixDAO', '472', '15602', '541', '2018-07-18 16:06:46');
INSERT INTO `twitters_data` VALUES ('194', '53', 'Wanchain', '202', '109397', '76', '2018-07-18 16:06:46');
INSERT INTO `twitters_data` VALUES ('195', '54', 'Hshare', '494', '12270', '55', '2018-07-18 16:07:04');
INSERT INTO `twitters_data` VALUES ('196', '56', 'Mithril ', '345', '17616', '134', '2018-07-18 16:07:05');
INSERT INTO `twitters_data` VALUES ('197', '58', 'Mixin ', '99', '10', '3282', '2018-07-18 16:07:25');
INSERT INTO `twitters_data` VALUES ('198', '55', 'DigixDAO', '472', '15602', '541', '2018-07-18 16:07:28');
INSERT INTO `twitters_data` VALUES ('199', '59', 'Bitcoin Private', '400', '105', '52040', '2018-07-18 16:07:45');
INSERT INTO `twitters_data` VALUES ('200', '56', 'Mithril ', '345', '17616', '134', '2018-07-18 16:08:01');
INSERT INTO `twitters_data` VALUES ('201', '60', 'Komodo', '2892', '91358', '87', '2018-07-18 16:08:06');
INSERT INTO `twitters_data` VALUES ('202', '61', 'Aion', '955', '52338', '1454', '2018-07-18 16:08:22');
INSERT INTO `twitters_data` VALUES ('203', '58', 'Mixin ', '99', '10', '3282', '2018-07-18 16:08:22');
INSERT INTO `twitters_data` VALUES ('204', '62', 'Huobi Token ', '2685', '72688', '335', '2018-07-18 16:08:41');
INSERT INTO `twitters_data` VALUES ('205', '59', 'Bitcoin Private', '400', '105', '52040', '2018-07-18 16:08:41');
INSERT INTO `twitters_data` VALUES ('206', '63', 'MaidSafeCoin ', '3515', '57963', '337', '2018-07-18 16:08:58');
INSERT INTO `twitters_data` VALUES ('207', '60', 'Komodo', '2892', '91358', '87', '2018-07-18 16:09:10');
INSERT INTO `twitters_data` VALUES ('208', '64', 'GXChain', '650', '11146', '316', '2018-07-18 16:09:17');
INSERT INTO `twitters_data` VALUES ('209', '61', 'Aion', '955', '52338', '1454', '2018-07-18 16:09:32');
INSERT INTO `twitters_data` VALUES ('210', '65', 'Nebulas ', '488', '23888', '41', '2018-07-18 16:09:41');
INSERT INTO `twitters_data` VALUES ('211', '62', 'Huobi Token ', '2685', '72688', '335', '2018-07-18 16:09:53');
INSERT INTO `twitters_data` VALUES ('212', '63', 'MaidSafeCoin ', '3515', '57963', '337', '2018-07-18 16:10:10');
INSERT INTO `twitters_data` VALUES ('213', '66', 'Ardor', '0', '0', '0', '2018-07-18 16:10:28');
INSERT INTO `twitters_data` VALUES ('214', '64', 'GXChain', '650', '11146', '316', '2018-07-18 16:10:30');
INSERT INTO `twitters_data` VALUES ('215', '65', 'Nebulas ', '488', '23888', '41', '2018-07-18 16:10:49');
INSERT INTO `twitters_data` VALUES ('216', '67', 'Loopring', '1595', '28174', '362', '2018-07-18 16:10:50');
INSERT INTO `twitters_data` VALUES ('217', '68', 'Aelf', '410', '23550', '101', '2018-07-18 16:11:15');
INSERT INTO `twitters_data` VALUES ('218', '66', 'Ardor', '0', '0', '0', '2018-07-18 16:11:30');
INSERT INTO `twitters_data` VALUES ('219', '69', 'Ark', '1308', '64461', '2687', '2018-07-18 16:11:33');
INSERT INTO `twitters_data` VALUES ('220', '70', 'MonaCoin', '0', '0', '0', '2018-07-18 16:11:49');
INSERT INTO `twitters_data` VALUES ('221', '67', 'Loopring', '1595', '28174', '362', '2018-07-18 16:11:52');
INSERT INTO `twitters_data` VALUES ('222', '68', 'Aelf', '410', '23550', '101', '2018-07-18 16:12:10');
INSERT INTO `twitters_data` VALUES ('223', '71', 'ReddCoin', '7698', '72899', '223', '2018-07-18 16:12:11');
INSERT INTO `twitters_data` VALUES ('224', '72', 'FunFair ', '545', '37099', '320', '2018-07-18 16:12:28');
INSERT INTO `twitters_data` VALUES ('225', '69', 'Ark', '1308', '64461', '2687', '2018-07-18 16:12:29');
INSERT INTO `twitters_data` VALUES ('226', '70', 'MonaCoin', '0', '0', '0', '2018-07-18 16:12:45');
INSERT INTO `twitters_data` VALUES ('227', '73', 'Kyber Network', '1227', '87471', '551', '2018-07-18 16:12:47');
INSERT INTO `twitters_data` VALUES ('228', '74', 'Loom Network', '750', '13431', '67', '2018-07-18 16:13:02');
INSERT INTO `twitters_data` VALUES ('229', '71', 'ReddCoin', '7698', '72899', '223', '2018-07-18 16:13:03');
INSERT INTO `twitters_data` VALUES ('230', '75', 'Emercoin', '157', '3371', '10', '2018-07-18 16:13:22');
INSERT INTO `twitters_data` VALUES ('231', '72', 'FunFair ', '545', '37099', '320', '2018-07-18 16:13:23');
INSERT INTO `twitters_data` VALUES ('232', '76', 'Dentacoin', '871', '18019', '487', '2018-07-18 16:13:39');
INSERT INTO `twitters_data` VALUES ('233', '73', 'Kyber Network', '1227', '87471', '551', '2018-07-18 16:13:39');
INSERT INTO `twitters_data` VALUES ('234', '77', 'MCO', '470', '65779', '58', '2018-07-18 16:13:58');
INSERT INTO `twitters_data` VALUES ('235', '74', 'Loom Network', '750', '13431', '67', '2018-07-18 16:13:58');
INSERT INTO `twitters_data` VALUES ('236', '78', 'WAX', '1595', '16984', '211', '2018-07-18 16:14:10');
INSERT INTO `twitters_data` VALUES ('237', '75', 'Emercoin', '157', '3371', '10', '2018-07-18 16:14:11');
INSERT INTO `twitters_data` VALUES ('238', '79', 'Gas', '1511', '452123', '1904', '2018-07-18 16:14:29');
INSERT INTO `twitters_data` VALUES ('239', '76', 'Dentacoin', '871', '18018', '487', '2018-07-18 16:14:30');
INSERT INTO `twitters_data` VALUES ('240', '81', 'Bancor ', '1560', '73197', '102', '2018-07-18 16:14:41');
INSERT INTO `twitters_data` VALUES ('241', '77', 'MCO', '470', '65778', '58', '2018-07-18 16:14:42');
INSERT INTO `twitters_data` VALUES ('242', '82', 'Cryptonex', '220', '31120', '17', '2018-07-18 16:14:59');
INSERT INTO `twitters_data` VALUES ('243', '78', 'WAX', '1595', '16984', '211', '2018-07-18 16:15:00');
INSERT INTO `twitters_data` VALUES ('244', '83', 'Veritaseum', '14972', '23197', '596', '2018-07-18 16:15:11');
INSERT INTO `twitters_data` VALUES ('245', '79', 'Gas', '1511', '452123', '1904', '2018-07-18 16:15:12');
INSERT INTO `twitters_data` VALUES ('246', '81', 'Bancor ', '1560', '73197', '102', '2018-07-18 16:15:30');
INSERT INTO `twitters_data` VALUES ('247', '85', 'CyberMiles', '426', '297343', '139', '2018-07-18 16:15:31');
INSERT INTO `twitters_data` VALUES ('248', '82', 'Cryptonex', '220', '31120', '17', '2018-07-18 16:15:42');
INSERT INTO `twitters_data` VALUES ('249', '86', 'Power Ledger', '3497', '86419', '2967', '2018-07-18 16:15:43');
INSERT INTO `twitters_data` VALUES ('250', '87', 'Ethos', '590', '60962', '991', '2018-07-18 16:16:01');
INSERT INTO `twitters_data` VALUES ('251', '83', 'Veritaseum', '14972', '23197', '596', '2018-07-18 16:16:01');
INSERT INTO `twitters_data` VALUES ('252', '88', 'MOAC', '255', '450', '741', '2018-07-18 16:16:13');
INSERT INTO `twitters_data` VALUES ('253', '85', 'CyberMiles', '426', '297344', '139', '2018-07-18 16:16:14');
INSERT INTO `twitters_data` VALUES ('254', '89', 'PIVX', '2478', '60270', '396', '2018-07-18 16:16:32');
INSERT INTO `twitters_data` VALUES ('255', '86', 'Power Ledger', '3497', '86419', '2967', '2018-07-18 16:16:32');
INSERT INTO `twitters_data` VALUES ('256', '87', 'Ethos', '590', '60962', '991', '2018-07-18 16:16:52');
INSERT INTO `twitters_data` VALUES ('257', '90', 'Decentraland', '573', '37407', '176', '2018-07-18 16:16:52');
INSERT INTO `twitters_data` VALUES ('258', '88', 'MOAC', '255', '450', '741', '2018-07-18 16:17:09');
INSERT INTO `twitters_data` VALUES ('259', '91', 'Dropil', '133', '6965', '86', '2018-07-18 16:17:10');
INSERT INTO `twitters_data` VALUES ('260', '92', 'Paypex', '112', '2108', '903', '2018-07-18 16:17:22');
INSERT INTO `twitters_data` VALUES ('261', '89', 'PIVX', '2478', '60270', '396', '2018-07-18 16:17:23');
INSERT INTO `twitters_data` VALUES ('262', '93', 'QASH', '1509', '21719', '730', '2018-07-18 16:17:44');
INSERT INTO `twitters_data` VALUES ('263', '90', 'Decentraland', '573', '37407', '176', '2018-07-18 16:17:44');
INSERT INTO `twitters_data` VALUES ('264', '91', 'Dropil', '133', '6965', '86', '2018-07-18 16:17:56');
INSERT INTO `twitters_data` VALUES ('265', '94', 'Polymath', '907', '28097', '167', '2018-07-18 16:17:59');
