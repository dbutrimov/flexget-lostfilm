import requests
import unittest
import yaml

import baibako


class TestBaibako(unittest.TestCase):
    def setUp(self):
        with open("test_config.yml", 'r') as stream:
            config = yaml.load(stream)
            self._username = config['secrets']['baibako']['username']
            self._password = config['secrets']['baibako']['password']

            self._auth = baibako.BaibakoAuth(self._username, self._password)
            self._requests = requests.session()
            self._requests.auth = self._auth

    def test_forums(self):
        forums = baibako.Baibako.get_forums(self._requests)
        for forum in forums:
            print(u"[{0}] {1}".format(forum.id, forum.title))

        self.assertRaises(Exception)

    def test_forum_topics(self):
        topics = baibako.Baibako.get_forum_topics(472, 'all', self._requests)
        for topic in topics:
            print(u"[{0}] {1}".format(topic.id, topic.title))

            topic_info = baibako.BaibakoParser.parse_topic_title(topic.title)
            print(u"{0} / {1} / {2} / {3}".format(
                topic_info.title,
                topic_info.alternative_titles[0],
                topic_info.get_episode_id(),
                topic_info.quality
            ))

        self.assertRaises(Exception)


if __name__ == '__main__':
    unittest.main()
