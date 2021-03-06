import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leaderboard.settings')
django.setup()

import time
import logging
from rethinkdb.errors import RqlDriverError
from leaderboardapp.models import Board, Player
from leaderboardapp.views import publish_board

logger = logging.getLogger('dblistener')

while True:
	try:
		for change in Player.get_all_changes():
			logger.debug('got change: %s' % change)
			try:
				row = change['new_val']
				board = Board.get(row['board'])
				publish_board(board)
			except Exception:
				logger.exception('failed to handle')
	except RqlDriverError:
		logger.exception('failed to connect')
		time.sleep(1)
