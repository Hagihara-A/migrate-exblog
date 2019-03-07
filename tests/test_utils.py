from unittest import TestCase
from migrate_exblog.utils import get_title_class, get_body_class, get_tail_class
from bs4 import BeautifulSoup
STRUCTURE = r"""<div class="post">
<div class="POST_HEAD" align="left">
<$postdate$>
</div>
<table border="0" cellpadding="0" cellspacing="0" width="500" align="center">
<tr><td width="400"><h2 class="POST_TTL"><$postsubject$></h2></td>
    <td width="99" align="right"><$postadmin type=1$></td></tr>
</table>
<div class="POST_BODY">
<$postcont$>
</div>
<div class="POST_TAIL" align="right"><$posttail$></div>
<$cmtjs$>
</div>"""


class TestUtils(TestCase):
    def setUp(self):
        self.soup = BeautifulSoup(STRUCTURE, 'html.parser')

    def test_get_title_class(self):
        actual = get_title_class(self.soup)
        self.assertEqual('POST_TTL', actual)

    def test_get_body_class(self):
        actual = get_body_class(self.soup)
        self.assertEqual('POST_BODY', actual)

    def test_get_tail_class(self):
        actual = get_tail_class(self.soup)
        self.assertEqual('POST_TAIL', actual)
