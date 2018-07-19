/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : localhost:3306
 Source Schema         : exper

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 19/07/2018 11:42:18
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for fb_data
-- ----------------------------
DROP TABLE IF EXISTS `fb_data`;
CREATE TABLE `fb_data`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fb_name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `likes_num` int(11) NULL DEFAULT NULL,
  `watches_num` int(11) NULL DEFAULT NULL,
  `coin_id` int(11) NULL DEFAULT NULL,
  `update_time` timestamp(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 95 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of fb_data
-- ----------------------------
INSERT INTO `fb_data` VALUES (1, 'Bitcoin', 0, 0, 1, '2018-07-19 11:08:48');
INSERT INTO `fb_data` VALUES (2, 'Ethereum', 139498, 148718, 2, '2018-07-19 11:08:59');
INSERT INTO `fb_data` VALUES (3, 'XRP', 125225, 136134, 3, '2018-07-19 11:09:07');
INSERT INTO `fb_data` VALUES (4, 'Bitcoin Cash', 17503, 19886, 4, '2018-07-19 11:09:20');
INSERT INTO `fb_data` VALUES (5, 'EOS', 11954, 14595, 5, '2018-07-19 11:09:30');
INSERT INTO `fb_data` VALUES (6, 'Litecoin', 0, 0, 6, '2018-07-19 11:09:30');
INSERT INTO `fb_data` VALUES (7, 'Stellar', 18739, 20924, 7, '2018-07-19 11:09:38');
INSERT INTO `fb_data` VALUES (8, 'Cardano', 19777, 23016, 8, '2018-07-19 11:09:48');
INSERT INTO `fb_data` VALUES (9, 'IOTA', 0, 0, 9, '2018-07-19 11:09:48');
INSERT INTO `fb_data` VALUES (10, 'Tether', 1586, 1878, 10, '2018-07-19 11:09:59');
INSERT INTO `fb_data` VALUES (11, 'TRON', 131001, 133753, 11, '2018-07-19 11:10:11');
INSERT INTO `fb_data` VALUES (12, 'NEO', 25949, 29697, 12, '2018-07-19 11:10:56');
INSERT INTO `fb_data` VALUES (13, 'Monero', 0, 0, 13, '2018-07-19 11:10:56');
INSERT INTO `fb_data` VALUES (14, 'Dash', 35590, 38382, 14, '2018-07-19 11:11:06');
INSERT INTO `fb_data` VALUES (15, 'Ethereum Classic', 0, 0, 15, '2018-07-19 11:11:06');
INSERT INTO `fb_data` VALUES (16, 'NEM', 0, 0, 16, '2018-07-19 11:11:06');
INSERT INTO `fb_data` VALUES (17, 'Binance Coin', 67097, 73704, 17, '2018-07-19 11:11:21');
INSERT INTO `fb_data` VALUES (18, 'VeChain', 0, 0, 18, '2018-07-19 11:11:21');
INSERT INTO `fb_data` VALUES (19, 'Tezos', 0, 0, 19, '2018-07-19 11:11:21');
INSERT INTO `fb_data` VALUES (20, 'OmiseGO', 9491, 10547, 20, '2018-07-19 11:11:31');
INSERT INTO `fb_data` VALUES (21, 'Qtum', 9617, 11195, 21, '2018-07-19 11:11:39');
INSERT INTO `fb_data` VALUES (22, 'Zcash', 0, 0, 22, '2018-07-19 11:11:39');
INSERT INTO `fb_data` VALUES (23, 'Ontology', 3445, 4342, 23, '2018-07-19 11:11:49');
INSERT INTO `fb_data` VALUES (24, 'Lisk', 27103, 28727, 24, '2018-07-19 11:11:58');
INSERT INTO `fb_data` VALUES (25, 'Bytecoin', 0, 0, 25, '2018-07-19 11:11:58');
INSERT INTO `fb_data` VALUES (26, 'ICON', 6403, 7496, 26, '2018-07-19 11:12:07');
INSERT INTO `fb_data` VALUES (27, 'Zilliqa ', 0, 0, 27, '2018-07-19 11:12:07');
INSERT INTO `fb_data` VALUES (28, 'Bitcoin Gold', 23435, 25750, 28, '2018-07-19 11:12:16');
INSERT INTO `fb_data` VALUES (29, '0x', 0, 0, 29, '2018-07-19 11:12:16');
INSERT INTO `fb_data` VALUES (30, 'Decred', 0, 0, 30, '2018-07-19 11:12:16');
INSERT INTO `fb_data` VALUES (31, 'BitShares', 0, 0, 31, '2018-07-19 11:12:16');
INSERT INTO `fb_data` VALUES (32, 'DigiByte', 20028, 21724, 32, '2018-07-19 11:12:25');
INSERT INTO `fb_data` VALUES (33, 'Aeternity', 2276, 2761, 33, '2018-07-19 11:12:35');
INSERT INTO `fb_data` VALUES (34, 'Maker', 0, 0, 34, '2018-07-19 11:12:35');
INSERT INTO `fb_data` VALUES (35, 'Siacoin', 0, 0, 35, '2018-07-19 11:12:35');
INSERT INTO `fb_data` VALUES (36, 'Steem', 26291, 27761, 36, '2018-07-19 11:12:45');
INSERT INTO `fb_data` VALUES (37, 'Augur', 17000, 17312, 37, '2018-07-19 11:12:58');
INSERT INTO `fb_data` VALUES (38, 'Verge ', 31249, 34690, 38, '2018-07-19 11:13:07');
INSERT INTO `fb_data` VALUES (39, 'Nano', 0, 0, 39, '2018-07-19 11:13:07');
INSERT INTO `fb_data` VALUES (40, 'Bytom', 254, 378, 40, '2018-07-19 11:13:15');
INSERT INTO `fb_data` VALUES (41, 'Bitcoin Diamond', 0, 0, 41, '2018-07-19 11:13:15');
INSERT INTO `fb_data` VALUES (42, 'Waltonchain', 0, 0, 43, '2018-07-19 11:13:19');
INSERT INTO `fb_data` VALUES (43, 'Pundi X', 105068, 105496, 44, '2018-07-19 11:13:28');
INSERT INTO `fb_data` VALUES (44, 'Dogecoin', 0, 0, 45, '2018-07-19 11:13:28');
INSERT INTO `fb_data` VALUES (45, 'Waves ', 73879, 76173, 47, '2018-07-19 11:13:43');
INSERT INTO `fb_data` VALUES (46, 'RChain', 0, 0, 48, '2018-07-19 11:13:43');
INSERT INTO `fb_data` VALUES (47, 'Golem', 0, 0, 49, '2018-07-19 11:13:43');
INSERT INTO `fb_data` VALUES (48, 'Populous ', 0, 0, 50, '2018-07-19 11:13:43');
INSERT INTO `fb_data` VALUES (49, 'Stratis ', 0, 0, 51, '2018-07-19 11:13:43');
INSERT INTO `fb_data` VALUES (50, 'Status', 10826, 11894, 52, '2018-07-19 11:13:52');
INSERT INTO `fb_data` VALUES (51, 'Wanchain', 16738, 18952, 53, '2018-07-19 11:14:00');
INSERT INTO `fb_data` VALUES (52, 'Hshare', 1581, 2110, 54, '2018-07-19 11:14:11');
INSERT INTO `fb_data` VALUES (53, 'DigixDAO', 0, 0, 55, '2018-07-19 11:14:11');
INSERT INTO `fb_data` VALUES (54, 'Mithril ', 2870, 3079, 56, '2018-07-19 11:14:19');
INSERT INTO `fb_data` VALUES (55, 'Mixin ', 4439, 4617, 58, '2018-07-19 11:14:34');
INSERT INTO `fb_data` VALUES (56, 'Bitcoin Private', 3706, 4230, 59, '2018-07-19 11:14:43');
INSERT INTO `fb_data` VALUES (57, 'Komodo', 15383, 16016, 60, '2018-07-19 11:14:53');
INSERT INTO `fb_data` VALUES (58, 'Aion', 22349, 22689, 61, '2018-07-19 11:15:01');
INSERT INTO `fb_data` VALUES (59, 'Huobi Token ', 3410, 3763, 62, '2018-07-19 11:15:17');
INSERT INTO `fb_data` VALUES (60, 'MaidSafeCoin ', 0, 0, 63, '2018-07-19 11:15:17');
INSERT INTO `fb_data` VALUES (61, 'GXChain', 11, 16, 64, '2018-07-19 11:15:27');
INSERT INTO `fb_data` VALUES (62, 'Nebulas ', 1699, 2091, 65, '2018-07-19 11:15:36');
INSERT INTO `fb_data` VALUES (63, 'Loopring', 0, 0, 67, '2018-07-19 11:15:44');
INSERT INTO `fb_data` VALUES (64, 'Aelf', 106, 121, 68, '2018-07-19 11:15:54');
INSERT INTO `fb_data` VALUES (65, 'Ark', 8133, 8881, 69, '2018-07-19 11:16:03');
INSERT INTO `fb_data` VALUES (66, 'MonaCoin', 0, 0, 70, '2018-07-19 11:16:03');
INSERT INTO `fb_data` VALUES (67, 'ReddCoin', 26778, 27989, 71, '2018-07-19 11:16:12');
INSERT INTO `fb_data` VALUES (68, 'Kyber Network', 6939, 7022, 73, '2018-07-19 11:16:28');
INSERT INTO `fb_data` VALUES (69, 'Loom Network', 0, 0, 74, '2018-07-19 11:16:28');
INSERT INTO `fb_data` VALUES (70, 'Emercoin', 1178, 1280, 75, '2018-07-19 11:16:38');
INSERT INTO `fb_data` VALUES (71, 'Dentacoin', 35365, 36342, 76, '2018-07-19 11:16:49');
INSERT INTO `fb_data` VALUES (72, 'MCO', 4304, 4984, 77, '2018-07-19 11:16:57');
INSERT INTO `fb_data` VALUES (73, 'WAX', 863, 1028, 78, '2018-07-19 11:17:07');
INSERT INTO `fb_data` VALUES (74, 'Gas', 27288, 29871, 79, '2018-07-19 11:17:16');
INSERT INTO `fb_data` VALUES (75, 'Nuls', 0, 0, 80, '2018-07-19 11:17:16');
INSERT INTO `fb_data` VALUES (76, 'Bancor ', 66456, 66905, 81, '2018-07-19 11:17:25');
INSERT INTO `fb_data` VALUES (77, 'Veritaseum', 5434, 5558, 83, '2018-07-19 11:17:39');
INSERT INTO `fb_data` VALUES (78, 'Kin', 0, 0, 84, '2018-07-19 11:17:39');
INSERT INTO `fb_data` VALUES (79, 'CyberMiles', 12929, 13591, 85, '2018-07-19 11:17:47');
INSERT INTO `fb_data` VALUES (80, 'Power Ledger', 20611, 22642, 86, '2018-07-19 11:17:56');
INSERT INTO `fb_data` VALUES (81, 'Ethos', 11016, 12466, 87, '2018-07-19 11:18:07');
INSERT INTO `fb_data` VALUES (82, 'MOAC', 33, 47, 88, '2018-07-19 11:18:18');
INSERT INTO `fb_data` VALUES (83, 'PIVX', 25909, 26324, 89, '2018-07-19 11:18:28');
INSERT INTO `fb_data` VALUES (84, 'Decentraland', 5560, 5980, 90, '2018-07-19 11:18:38');
INSERT INTO `fb_data` VALUES (85, 'Dropil', 7267, 7524, 91, '2018-07-19 11:18:47');
INSERT INTO `fb_data` VALUES (86, 'Paypex', 622, 624, 92, '2018-07-19 11:18:56');
INSERT INTO `fb_data` VALUES (87, 'QASH', 38173, 39502, 93, '2018-07-19 11:19:04');
INSERT INTO `fb_data` VALUES (88, 'Polymath', 34974, 36185, 94, '2018-07-19 11:19:13');
INSERT INTO `fb_data` VALUES (89, 'ZenCash', 2829, 3113, 95, '2018-07-19 11:19:24');
INSERT INTO `fb_data` VALUES (90, 'Cortex', 316, 377, 96, '2018-07-19 11:19:34');
INSERT INTO `fb_data` VALUES (91, 'Noah Coin', 44114, 45716, 97, '2018-07-19 11:19:46');
INSERT INTO `fb_data` VALUES (92, 'Factom ', 5268, 5630, 98, '2018-07-19 11:20:05');
INSERT INTO `fb_data` VALUES (93, 'Theta Token', 46918, 51547, 99, '2018-07-19 11:20:18');
INSERT INTO `fb_data` VALUES (94, 'Elastos', 15798, 16105, 100, '2018-07-19 11:20:26');

SET FOREIGN_KEY_CHECKS = 1;
