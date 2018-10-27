import datetime
import os
import unittest
from unittest.mock import patch, mock_open

import gerry


class DatetimeToString(unittest.TestCase):
    def test_datetime_to_string(self):
        date = datetime.datetime(2018, 1, 1)
        self.assertEqual(gerry.datetime_to_string(
            date), '2018-01-01 00:00:00.000')

        date = datetime.datetime(2018, 1, 1, 20, 0, 0)
        self.assertEqual(gerry.datetime_to_string(
            date), '2018-01-01 20:00:00.000')


class CreateTimeFrames(unittest.TestCase):
    def test_create_time_frames_year(self):
        start_date = datetime.datetime(2017, 1, 1)
        end_date = datetime.datetime(2018, 1, 1)
        timeframes = gerry.create_time_frames(
            start_date, end_date, datetime.timedelta(hours=24))
        self.assertEqual(len(timeframes), 365)

    def test_create_time_frames_day(self):
        start_date = datetime.datetime(2017, 1, 1)
        end_date = datetime.datetime(2017, 1, 2)
        timeframes = gerry.create_time_frames(
            start_date, end_date, datetime.timedelta(hours=1))
        self.assertEqual(len(timeframes), 24)


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://too-many-requests.com':
        raise gerry.requests.exceptions.RequestException(response=MockResponse({"key1": "value1"}, 429))
    elif args[0] == 'http://no-response.com':
        raise gerry.requests.exceptions.RequestException(response=None)


class Gerry(unittest.TestCase):

    @patch('os.makedirs')
    def setUp(self, mock_makedirs):
        mock_makedirs.return_value = True
        self.gerry = gerry.Gerry('gerrit', 'https://gerrit-review.googlesource.com',
                                 datetime.datetime(2018, 6, 1), datetime.datetime(2018, 6, 2), './gerry_data/')

    @patch('time.sleep')
    def test_wait_for_server(self, mock_sleep):
        gerry.Gerry.wait_for_server(000)
        self.assertFalse(mock_sleep.called)

        gerry.Gerry.wait_for_server(429)
        self.assertTrue(mock_sleep.called)

        gerry.Gerry.wait_for_server(500)
        self.assertTrue(mock_sleep.called)

        gerry.Gerry.wait_for_server(501)
        self.assertTrue(mock_sleep.called)

    @patch('gerry.log')
    @patch('gerry.requests.get', side_effect=mocked_requests_get)
    @patch('gerry.Gerry.wait_for_server')
    def test_handle_exception(self, mock_wait_for_server, mock_get, mock_log):
        try:
            mock_get("http://too-many-requests.com")
        except Exception as exception:
            gerry.Gerry.handle_exception(exception, 'change 42')
        mock_wait_for_server.assert_called_once_with(429)
        self.assertTrue(mock_log.error.called)

        try:
            mock_get("http://no-response.com")
        except Exception as exception:
            gerry.Gerry.handle_exception(exception, 'change 42')
        self.assertTrue(mock_log.error.called)

        try:
            raise gerry.json.JSONDecodeError('', '', 0)
        except Exception as exception:
            gerry.Gerry.handle_exception(exception, 'change 42')
        self.assertTrue(mock_log.error.called)

        try:
            raise Exception()
        except Exception as exception:
            gerry.Gerry.handle_exception(exception, 'change 42')
        self.assertTrue(mock_log.error.called)
        mock_wait_for_server.assert_called_once_with(429)

    def test_get_changes(self):
        changes = self.gerry.get_changes(
            datetime.datetime.strptime('2018-06-01', '%Y-%m-%d'))
        self.assertEqual(len(changes), 21)
        self.assertEqual(changes[0]['change_id'],
                         'Ib051dd347eaea2c77ae6c403ebf76bed4b9b4b9c')

    def test_get_changes_no_data(self):
        changes = self.gerry.get_changes(
            datetime.datetime.strptime('5018-06-01', '%Y-%m-%d'))
        self.assertEqual(len(changes), 0)

    @patch('json.dump')
    @patch("builtins.open", new_callable=mock_open)
    def test_get_change(self, mock_file, mock_dump):
        self.gerry.get_change(109611, 'folder')
        mock_file.assert_any_call(os.path.join('folder', '109611.json'), 'w')
        self.assertEqual(
            mock_dump.call_args[0][0]['change_id'], 'Ic7bc5ad2e57eef27b0d2e13523be78e8a2d0a65c')

    @patch('os.makedirs')
    @patch('glob.glob')
    @patch('os.listdir')
    @patch('gerry.Gerry.get_change')
    def test_run(self, mock_get_change, mock_listdir,
                 mock_glob, mock_makedirs):
        mock_makedirs.return_value = True
        mock_glob.return_value = [os.path.join(self.gerry.directory, self.gerry.name, 'changes', '2018-06-01'),
                                  os.path.join(self.gerry.directory, self.gerry.name, 'changes', '2018-06-02')]
        mock_listdir.return_value = False

        self.gerry.run()
        # valid change number from 2018-06-01
        mock_get_change.assert_any_call(109611, mock_glob.return_value[0])
        # valid change number from 2018-06-02
        mock_get_change.assert_any_call(181990, mock_glob.return_value[1])


if __name__ == '__main__':
    unittest.main()
