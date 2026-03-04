"""Tests for gmail.fetcher module."""

from __future__ import annotations

from datetime import datetime, timedelta

from gmail.fetcher import build_query, fetch_emails, get_attachments


def test_build_query_contains_subject_and_after_timestamp() -> None:
    """Build query with subject and 24-hour `after` timestamp."""
    query = build_query('Relatorio')

    assert query.startswith('subject:Relatorio after:')
    timestamp = int(query.split('after:')[1])
    now_ts = int(datetime.now().timestamp())
    day_ago_ts = int((datetime.now() - timedelta(hours=24)).timestamp())
    assert day_ago_ts - 5 <= timestamp <= now_ts


def test_fetch_emails_paginates_all_results(mocker) -> None:
    """Fetch all pages returned by Gmail API list endpoint."""
    service = mocker.Mock()
    messages_api = service.users.return_value.messages.return_value

    first_page = {
        'messages': [{'id': 'm1'}],
        'nextPageToken': 'next-token',
    }
    second_page = {'messages': [{'id': 'm2'}, {'id': 'm3'}]}

    messages_api.list.return_value.execute.side_effect = [
        first_page,
        second_page,
    ]

    result = fetch_emails(service, 'subject:test after:123')

    assert [msg['id'] for msg in result] == ['m1', 'm2', 'm3']
    assert messages_api.list.call_count == 2
    first_call = messages_api.list.call_args_list[0].kwargs
    second_call = messages_api.list.call_args_list[1].kwargs
    assert first_call['q'] == 'subject:test after:123'
    assert first_call['pageToken'] is None
    assert second_call['pageToken'] == 'next-token'


def test_get_attachments_returns_only_xlsx(mocker) -> None:
    """Filter attachment list to `.xlsx` files only."""
    service = mocker.Mock()
    messages_api = service.users.return_value.messages.return_value

    messages_api.get.return_value.execute.return_value = {
        'payload': {
            'parts': [
                {
                    'filename': 'report.xlsx',
                    'body': {'attachmentId': 'a1'},
                },
                {
                    'filename': 'ignore.pdf',
                    'body': {'attachmentId': 'a2'},
                },
                {
                    'filename': 'summary.XLSX',
                    'body': {'attachmentId': 'a3'},
                },
            ]
        }
    }

    attachments = get_attachments(service, 'message-id')

    assert attachments == [
        {'filename': 'report.xlsx', 'attachment_id': 'a1'},
        {'filename': 'summary.XLSX', 'attachment_id': 'a3'},
    ]
