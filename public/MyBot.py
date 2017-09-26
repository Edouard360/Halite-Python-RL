import sys

mode = 'server' if (len(sys.argv) == 1) else 'local'
mode = 'local'  # TODO remove forcing
if mode == 'server':  # 'server' mode
    import hlt
else:  # 'local' mode
    from networking.hlt_networking import HLT

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    hlt = HLT(port=port)

from public.models.bot.trainedBot import TrainedBot

import tensorflow as tf

tf.reset_default_graph()

with tf.device("/cpu:0"):
    with tf.variable_scope('global'):
        bot = TrainedBot()
    global_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='global')
    saver = tf.train.Saver(global_variables)
    init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    try:
        saver.restore(sess, 'models/' + bot.agent.name)
    except Exception:
        print("Model not found - initiating new one")

    while True:
        myID, game_map = hlt.get_init()
        bot.setID(myID)
        hlt.send_init("OpponentBot")

        while (mode == 'server' or hlt.get_string() == 'Get map and play!'):
            game_map.get_frame(hlt.get_string())
            moves = bot.compute_moves(game_map, sess)
            hlt.send_frame(moves)
