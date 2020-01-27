import unittest

import dao


class DaoTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('setup')
        cls.vid = 1
        cls.actor = dao.Actor(
            name='小田切让',
            avatar='这是avatar'
        )
        cls.actor2 = dao.Actor(
            name='石森章太郎',
            avatar='这是avatar'
        )
        cls.download = dao.Download(
            url='magnet://xxxxxx',
            type='磁力'
        )
        cls.download2 = dao.Download(
            url='http://yun.baidu.com',
            type='百度云'
        )
        cls.play = dao.Play(
            url='https://bilibili.com'
        )
        cls.vod = dao.Vod(
            title='假面骑士',
            cover="这是cover",
            intro="这是intro",
            actors=[cls.actor, cls.actor2],
            downloads=[cls.download, cls.download2],
            play_bilibili=cls.play
        )
        dao.drop_tables()
        dao.create_tables()

    @classmethod
    def tearDownClass(cls):
        print('teardown')
        dao.close_session()

    # 测试用例默认按方法名首字母顺序执行, 所以加上了1，2，3
    def test_1_insert_vod(self):
        vod = dao.insert_vod(self.vod)
        self.assertEqual(self.vid, vod.id)
        self.vod = vod

    def test_2_get_actors_by_vod_title(self):
        actors = dao.get_actors_by_vod_title('假面骑士')
        aids = [actor.id for actor in actors]
        self.assertEqual(2, len(aids))

    def test_3_get_actors_by_vod_title_with_relationship(self):
        actors = dao.get_actors_by_vod_title_with_relationship('假面骑士')
        aids = [actor.id for actor in actors]
        self.assertEqual(2, len(aids))

    def test_4_get_vods_by_actor_name_with_backref(self):
        vods = dao.get_vods_by_actor_name_with_backref('小田切让')
        vids = [vod.id for vod in vods]
        self.assertEqual(1, len(vids))

    def test_5_get_play_by_vod_id(self):
        play = dao.get_play_by_vod_id_with_relationship(1)
        self.assertEqual(1, play.id)

    def test_6_get_vod_by_play_id(self):
        vod = dao.get_vod_by_play_id_with_backref(1)
        self.assertEqual(1, vod.id)

    def test_7_get_downloads_by_vod_id_with_relationship(self):
        downloads = dao.get_downloads_by_vod_id_with_relationship(1)
        dids = [download.id for download in downloads]
        self.assertEqual(2, len(dids))

    def test_8_get_vod_by_download_id_with_backref(self):
        vod = dao.get_vod_by_download_id_with_backref(1)
        self.assertEqual(1, vod.id)

    def test_9_update_vod(self):
        self.vod.title = '奥特曼'
        dao.update_vod(self.vod)
        self.assertEqual('奥特曼', dao.get_vod(1).title)

    def test_90_delete_vod(self):
        dao.delete_vod(self.vod)
        self.assertIsNone(dao.get_vod(1))


if __name__ == '__main__':
    unittest.main()
