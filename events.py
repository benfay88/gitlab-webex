#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

def event_handler(msg):
    """
    receives gitlab message and executes the appropriate formatter
    """

    if os.getenv("DEBUG"):
        print(msg)

    handler_map = {
        'push': push_formatter,
        'issue': issue_formatter,
        'pipeline': pipeline_formatter,
        'note': note_formatter,
        'build': builds_formatter,
        'merge_request': merge_request_formatter
    }
    object_kind = msg['object_kind']
    message = handler_map[object_kind](msg)
    return message

# Push function
def push_formatter(msg):
    message = "### {} just pushed commits(s) in [{}]({})\n".format(msg['user'],
                                                                   msg['project']['path_with_namespace'],
                                                                   msg['project']['git_http_url'])                                             
    for commit in msg['commits']:
        commit = commit['message']
        commit = commit.encode('utf-8')
        message += "> [{}]({})\n".format(commit, commit['url'])
    return message

# Issue function
def issue_formatter(msg):
    issue = msg['object_attributes']
    title = msg['object_attributes']['title']
    title = title.encode('utf-8')
    message = "###{} just {} an issue in [{}]({})\n".format(msg['user']['username'],
                                                        issue['state'],
                                                        msg['project']['path_with_namespace'], 
                                                        msg['project']['git_http_url'])                                                   
    message += "> *[{}]({})*\n".format(title, issue['url'])
    if msg['labels']:
        message += " : Labels: "
        for l in msg['labels']:
            message += "{} ".format(l['title'])

    return message

# Pipeline status function
def pipeline_formatter(msg):
    repo_name = msg['project']['path_with_namespace']
    repo_url = msg['project']['web_url']
    pipeline_id = msg['object_attributes']['id']
    pipeline_url = repo_url + '/pipelines/{}'.format(pipeline_id)
    commit_msg = msg['commit']['message']
    commit_msg = commit_msg.encode('utf-8')
    commit_url = msg['commit']['url']

    sparkmsg = "## Pipeline update for [#{0}]({1})"
    sparkmsg += "\n\n[{2}]({3})"
    sparkmsg += "\n\n### Build Job Status"

    sparkmsg = sparkmsg.format(pipeline_id, pipeline_url, commit_msg, commit_url)

    for build in msg['builds']:
        sparkmsg += "\n\n* **{}:** {}".format(build['name'], build['status'])

    return sparkmsg

# Note function
def note_formatter(msg):
    repo_url = msg['project']['web_url']
    repo = msg['project']['path_with_namespace']
    note = msg['object_attributes']['note']
    note = note.encode('utf-8')
    note_type = msg['object_attributes']['noteable_type']
    note_url = msg['object_attributes']['url']
    user = msg['user']['username']

    if note_type == "Issue":
        issue = msg['issue']['iid']
        sparkmsg = ""
        sparkmsg += "### {} commented on issue [{}]({}) in {}".format(user, issue, note_url, repo)
        sparkmsg += "\n\n> {}".format(note)
        return sparkmsg
    elif note_type == "MergeRequest":
        merge = msg['merge_request']['iid']
        sparkmsg = ""
        sparkmsg += "### {} commented on merge request [{}]({})".format(user, merge, note_url)
        sparkmsg += "\n\n> {}".format(note)
        return sparkmsg

# Build function
def builds_formatter(msg):
    build = msg
    status = build['build_status']
    build_id = build['build_id']
    stage = build['build_stage']
    repo = build['project_name']
    commit_msg = build['commit']['message']
    commit_msg = commit_msg.encode('utf-8')
    repo_url = build['repository']['homepage'] + '/pipelines'
    sparkmsg = ""
    sparkmsg += "## Build update for build {}\n".format(build_id)
    sparkmsg += "\n\n**Repostory**: [{}]({})".format(repo, repo_url)
    sparkmsg += "\n\n**Status**: {}".format(status)
    sparkmsg += "\n\n**Stage**: {}".format(stage)
    sparkmsg += "\n\n**Commit Message**: {}".format(commit_msg)

    return None

# MR function
def merge_request_formatter(msg):
    mr = msg['object_attributes']
    source_branch = mr['source_branch']
    target_branch = mr['target_branch']
    user = msg['user']['username']
    source_repo = mr['source']['path_with_namespace']
    target_repo = mr['target']['path_with_namespace']
    target_repo_url = mr['target']['homepage']
    state = mr['state']
    title = mr['title']
    title = title.encode('utf-8')
    merge_id = mr['iid']
    url = mr['url']
    target_repo = "[{}]({})".format(target_repo, target_repo_url)
    message = ""
    message += "### {} just {} [merge request #{}]({}) in {}".format(user, state, merge_id, url, target_repo)
    message += "\n\n> *{}*".format(title)
    return message
