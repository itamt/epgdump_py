#!/usr/bin/python
# -*- coding: utf-8 -*-

READ_PACKETS_MAX = 700000  # => 700000*188 = 131.6 MB

TYPE_DEGITAL = ''
TYPE_BS = 'BS_'
TYPE_CS = 'CS_'

ONID_BS = 4
ONID_CS1 = 6
ONID_CS2 = 7

EIT_PID = (0x12, 0x26, 0x27)
SDT_PID = (0x11,)

TAG_SED = 0x4D  # Short event descriptor
TAG_EED = 0x4E  # Extended event descriptor
TAG_CD = 0x54  # Content descriptor
TAG_SD = 0x48  # Service descriptor

CONTENT_TYPE = {
    0x0: ('ニュース／報道',
          {
              0x0: '定時・総合',
              0x1: '天気',
              0x2: '特集・ドキュメント',
              0x3: '政治・国会',
              0x4: '経済・市況',
              0x5: '海外・国際',
              0x6: '解説',
              0x7: '討論・会談',
              0x8: '報道特番',
              0x9: 'ローカル・地域',
              0xA: '交通',
              0xF: 'その他',
          }),
    0x1: ('スポーツ',
          {
              0x0: 'スポーツニュース',
              0x1: '野球',
              0x2: 'サッカー',
              0x3: 'ゴルフ',
              0x4: 'その他の球技',
              0x5: '相撲・格闘技',
              0x6: 'オリンピック・国際大会',
              0x7: 'マラソン・陸上・水泳',
              0x8: 'モータースポーツ',
              0x9: 'マリン・ウィンタースポーツ',
              0xA: '競馬・公営競技',
              0xF: 'その他',
          }),
    0x2: ('情報／ワイドショー',
          {
              0x0: '芸能・ワイドショー',
              0x1: 'ファッション',
              0x2: '暮らし・住まい',
              0x3: '健康・医療',
              0x4: 'ショッピング・通販',
              0x5: 'グルメ・料理',
              0x6: 'イベント',
              0x7: '番組紹介・お知らせ',
              0xF: 'その他',
          }),
    0x3: ('ドラマ',
          {
              0x0: '国内ドラマ',
              0x1: '海外ドラマ',
              0x2: '時代劇',
              0xF: 'その他',
          }),
    0x4: ('音楽',
          {
              0x0: '国内ロック・ポップス',
              0x1: '海外ロック・ポップス',
              0x2: 'クラシック・オペラ',
              0x3: 'ジャズ・フュージョン',
              0x4: '歌謡曲・演歌',
              0x5: 'ライブ・コンサート',
              0x6: 'ランキング・リクエスト',
              0x7: 'カラオケ・のど自慢',
              0x8: '民謡・邦楽',
              0x9: '童謡・キッズ',
              0xA: '民族音楽・ワールドミュージック',
              0xF: 'その他',
          }),
    0x5: ('バラエティ',
          {
              0x0: 'クイズ',
              0x1: 'ゲーム',
              0x2: 'トークバラエティ',
              0x3: 'お笑い・コメディ',
              0x4: '音楽バラエティ',
              0x5: '旅バラエティ',
              0x6: '料理バラエティ',
              0xF: 'その他',
          }),
    0x6: ('映画',
          {
              0x0: '洋画',
              0x1: '邦画',
              0x2: 'アニメ',
              0xF: 'その他',
          }),
    0x7: ('アニメ／特撮',
          {
              0x0: '国内アニメ',
              0x1: '海外アニメ',
              0x2: '特撮',
              0xF: 'その他',
          }),
    0x8: ('ドキュメンタリー／教養',
          {
              0x0: '社会・時事',
              0x1: '歴史・紀行',
              0x2: '自然・動物・環境',
              0x3: '宇宙・科学・医学',
              0x4: 'カルチャー・伝統文化',
              0x5: '文学・文芸',
              0x6: 'スポーツ',
              0x7: 'ドキュメンタリー全般',
              0x8: 'インタビュー・討論',
              0xF: 'その他',
          }),
    0x9: ('劇場／公演',
          {
              0x0: '現代劇・新劇',
              0x1: 'ミュージカル',
              0x2: 'ダンス・バレエ',
              0x3: '落語・演芸',
              0x4: '歌舞伎・古典',
              0xF: 'その他',
          }),
    0xA: ('趣味／教育',
          {
              0x0: '旅・釣り・アウトドア',
              0x1: '園芸・ペット・手芸',
              0x2: '音楽・美術・工芸',
              0x3: '囲碁・将棋',
              0x4: '麻雀・パチンコ',
              0x5: '車・オートバイ',
              0x6: 'コンピュータ・ＴＶゲーム',
              0x7: '会話・語学',
              0x8: '幼児・小学生',
              0x9: '中学生・高校生',
              0xA: '大学生・受験',
              0xB: '生涯教育・資格',
              0xC: '教育問題',
              0xF: 'その他',
          }),
    0xB: ('福祉',
          {
              0x0: '高齢者',
              0x1: '障害者',
              0x2: '社会福祉',
              0x3: 'ボランティア',
              0x4: '手話',
              0x5: '文字（字幕）',
              0x6: '音声解説',
              0xF: 'その他',
          }),
    0xE: ('拡張',
          {
              0x0: 'BS/地上デジタル放送用番組付属情報',
              0x1: '広帯域CS デジタル放送用拡張',
              0x2: '衛星デジタル音声放送用拡張',
              0x3: 'サーバー型番組付属情報',
              0x4: 'IP 放送用番組付属情報',
          }),
    0xF: ('その他',
          {
          }),
    # 拡張ジャンル from xtne6f/EDCB: https://github.com/xtne6f/EDCB/commit/13bb6284dc5937e3f6edead4ed0917c393a94de2
    0x70: ('スポーツ(CS)',
           {
               0x0: 'テニス',
               0x1: 'バスケットボール',
               0x2: 'ラグビー',
               0x3: 'アメリカンフットボール',
               0x4: 'ボクシング',
               0x5: 'プロレス',
               0xF: 'その他',
           }),
    0x71: ('洋画(CS)',
           {
               0x0: 'アクション',
               0x1: 'SF／ファンタジー',
               0x2: 'コメディー',
               0x3: 'サスペンス／ミステリー',
               0x4: '恋愛／ロマンス',
               0x5: 'ホラー／スリラー',
               0x6: 'ウエスタン',
               0x7: 'ドラマ／社会派ドラマ',
               0x8: 'アニメーション',
               0x9: 'ドキュメンタリー',
               0xA: 'アドベンチャー／冒険',
               0xB: 'ミュージカル／音楽映画',
               0xC: 'ホームドラマ',
               0xF: 'その他',
           }),
    0x72: ('邦画(CS)',
           {
               0x0: 'アクション',
               0x1: 'SF／ファンタジー',
               0x2: 'お笑い／コメディー',
               0x3: 'サスペンス／ミステリー',
               0x4: '恋愛／ロマンス',
               0x5: 'ホラー／スリラー',
               0x6: '青春／学園／アイドル',
               0x7: '任侠／時代劇',
               0x8: 'アニメーション',
               0x9: 'ドキュメンタリー',
               0xA: 'アドベンチャー／冒険',
               0xB: 'ミュージカル／音楽映画',
               0xC: 'ホームドラマ',
               0xF: 'その他',
           }),
}

CRC_32_MPEG = (
    0x00000000, 0x04c11db7, 0x09823b6e, 0x0d4326d9,
    0x130476dc, 0x17c56b6b, 0x1a864db2, 0x1e475005,
    0x2608edb8, 0x22c9f00f, 0x2f8ad6d6, 0x2b4bcb61,
    0x350c9b64, 0x31cd86d3, 0x3c8ea00a, 0x384fbdbd,
    0x4c11db70, 0x48d0c6c7, 0x4593e01e, 0x4152fda9,
    0x5f15adac, 0x5bd4b01b, 0x569796c2, 0x52568b75,
    0x6a1936c8, 0x6ed82b7f, 0x639b0da6, 0x675a1011,
    0x791d4014, 0x7ddc5da3, 0x709f7b7a, 0x745e66cd,
    0x9823b6e0, 0x9ce2ab57, 0x91a18d8e, 0x95609039,
    0x8b27c03c, 0x8fe6dd8b, 0x82a5fb52, 0x8664e6e5,
    0xbe2b5b58, 0xbaea46ef, 0xb7a96036, 0xb3687d81,
    0xad2f2d84, 0xa9ee3033, 0xa4ad16ea, 0xa06c0b5d,
    0xd4326d90, 0xd0f37027, 0xddb056fe, 0xd9714b49,
    0xc7361b4c, 0xc3f706fb, 0xceb42022, 0xca753d95,
    0xf23a8028, 0xf6fb9d9f, 0xfbb8bb46, 0xff79a6f1,
    0xe13ef6f4, 0xe5ffeb43, 0xe8bccd9a, 0xec7dd02d,
    0x34867077, 0x30476dc0, 0x3d044b19, 0x39c556ae,
    0x278206ab, 0x23431b1c, 0x2e003dc5, 0x2ac12072,
    0x128e9dcf, 0x164f8078, 0x1b0ca6a1, 0x1fcdbb16,
    0x018aeb13, 0x054bf6a4, 0x0808d07d, 0x0cc9cdca,
    0x7897ab07, 0x7c56b6b0, 0x71159069, 0x75d48dde,
    0x6b93dddb, 0x6f52c06c, 0x6211e6b5, 0x66d0fb02,
    0x5e9f46bf, 0x5a5e5b08, 0x571d7dd1, 0x53dc6066,
    0x4d9b3063, 0x495a2dd4, 0x44190b0d, 0x40d816ba,
    0xaca5c697, 0xa864db20, 0xa527fdf9, 0xa1e6e04e,
    0xbfa1b04b, 0xbb60adfc, 0xb6238b25, 0xb2e29692,
    0x8aad2b2f, 0x8e6c3698, 0x832f1041, 0x87ee0df6,
    0x99a95df3, 0x9d684044, 0x902b669d, 0x94ea7b2a,
    0xe0b41de7, 0xe4750050, 0xe9362689, 0xedf73b3e,
    0xf3b06b3b, 0xf771768c, 0xfa325055, 0xfef34de2,
    0xc6bcf05f, 0xc27dede8, 0xcf3ecb31, 0xcbffd686,
    0xd5b88683, 0xd1799b34, 0xdc3abded, 0xd8fba05a,
    0x690ce0ee, 0x6dcdfd59, 0x608edb80, 0x644fc637,
    0x7a089632, 0x7ec98b85, 0x738aad5c, 0x774bb0eb,
    0x4f040d56, 0x4bc510e1, 0x46863638, 0x42472b8f,
    0x5c007b8a, 0x58c1663d, 0x558240e4, 0x51435d53,
    0x251d3b9e, 0x21dc2629, 0x2c9f00f0, 0x285e1d47,
    0x36194d42, 0x32d850f5, 0x3f9b762c, 0x3b5a6b9b,
    0x0315d626, 0x07d4cb91, 0x0a97ed48, 0x0e56f0ff,
    0x1011a0fa, 0x14d0bd4d, 0x19939b94, 0x1d528623,
    0xf12f560e, 0xf5ee4bb9, 0xf8ad6d60, 0xfc6c70d7,
    0xe22b20d2, 0xe6ea3d65, 0xeba91bbc, 0xef68060b,
    0xd727bbb6, 0xd3e6a601, 0xdea580d8, 0xda649d6f,
    0xc423cd6a, 0xc0e2d0dd, 0xcda1f604, 0xc960ebb3,
    0xbd3e8d7e, 0xb9ff90c9, 0xb4bcb610, 0xb07daba7,
    0xae3afba2, 0xaafbe615, 0xa7b8c0cc, 0xa379dd7b,
    0x9b3660c6, 0x9ff77d71, 0x92b45ba8, 0x9675461f,
    0x8832161a, 0x8cf30bad, 0x81b02d74, 0x857130c3,
    0x5d8a9099, 0x594b8d2e, 0x5408abf7, 0x50c9b640,
    0x4e8ee645, 0x4a4ffbf2, 0x470cdd2b, 0x43cdc09c,
    0x7b827d21, 0x7f436096, 0x7200464f, 0x76c15bf8,
    0x68860bfd, 0x6c47164a, 0x61043093, 0x65c52d24,
    0x119b4be9, 0x155a565e, 0x18197087, 0x1cd86d30,
    0x029f3d35, 0x065e2082, 0x0b1d065b, 0x0fdc1bec,
    0x3793a651, 0x3352bbe6, 0x3e119d3f, 0x3ad08088,
    0x2497d08d, 0x2056cd3a, 0x2d15ebe3, 0x29d4f654,
    0xc5a92679, 0xc1683bce, 0xcc2b1d17, 0xc8ea00a0,
    0xd6ad50a5, 0xd26c4d12, 0xdf2f6bcb, 0xdbee767c,
    0xe3a1cbc1, 0xe760d676, 0xea23f0af, 0xeee2ed18,
    0xf0a5bd1d, 0xf464a0aa, 0xf9278673, 0xfde69bc4,
    0x89b8fd09, 0x8d79e0be, 0x803ac667, 0x84fbdbd0,
    0x9abc8bd5, 0x9e7d9662, 0x933eb0bb, 0x97ffad0c,
    0xafb010b1, 0xab710d06, 0xa6322bdf, 0xa2f33668,
    0xbcb4666d, 0xb8757bda, 0xb5365d03, 0xb1f740b4
)
