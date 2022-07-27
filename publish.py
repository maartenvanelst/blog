#!/usr/bin/python3

'''
Note that part of this script is adapted code, 
the original author is marked in the comments.
'''

import os
import glob
import shutil
import subprocess

if __name__ == '__main__':
	''' This script should:
		[_] copy posts to target dir
		[_] Convert all image assets to .png
		[_] Replace markdown image headers with base64 version of png data
		[_] Encrypt markdown content in correct posts using the javascript encryption
		[_] Do success check on relevant posts
	'''

	ORIGIN_DIR = '../blog-src/_posts'
	TARGET_DIR = "./_posts"

	print('Copying posts...')
	for file in os.listdir(ORIGIN_DIR):
		shutil.copy(f'{ORIGIN_DIR}/{file}', f'{TARGET_DIR}/{file}')
		print(f'Copied {file}')

	'''
	tag_generator.py
	Copyright 2017 Long Qian
	Contact: lqian8@jhu.edu
	This script creates tags for your Jekyll blog hosted by Github page.
	No plugins required.

	Adapted by Maarten van Elst
	'''

	post_dir = '_posts/'
	draft_dir = '_drafts/'
	tag_dir = 'tag/'

	filenames = glob.glob(post_dir + '*md')
	filenames = filenames + glob.glob(draft_dir + '*md')

	total_tags = []

	for filename in filenames:
		f = open(filename, 'r')
		crawl = False
		for line in f:
			if crawl:
				current_tags = line.strip().split(':')
				if current_tags[0] == 'tags':
					if (current_tags[1].strip().startswith('[')):
						clean_tag = ''.join(
							c for c in current_tags[1] if c not in '[]')
						list_tags = map(str.strip, clean_tag.split(','))
						total_tags.extend(list_tags)
					else:
						list_tags = map(str.strip, current_tags[1].strip().split())
						total_tags.extend(list_tags)
					crawl = False
					break
			if line.strip() == '---':
				if not crawl:
					crawl = True
				else:
					crawl = False
					break
		f.close()
	total_tags_set = set(total_tags)

	old_tags = glob.glob(tag_dir + '*.md')
	for tag in old_tags:
		os.remove(tag)

	if not os.path.exists(tag_dir):
		os.makedirs(tag_dir)

	for tag in total_tags_set:
		tag_filename = tag_dir + tag.replace(' ', '_') + '.md'
		f = open(tag_filename, 'a')
		write_str = '---\nlayout: tagpage\ntitle: \"Tag: ' + tag + '\"\ntag: ' + tag + '\nrobots: noindex\n---\n'
		f.write(write_str)
		f.close()

	print("Tag\tcount\n-------------")
	for tag in total_tags_set:
		print(f"{tag}\t", total_tags.count(tag))
	print("-------------\ntotal\t", total_tags_set.__len__())

	'''
	End of adapted tag generator code.
	'''
