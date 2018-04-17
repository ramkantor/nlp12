import math


def viterbi(obs, states, start_p, trans_p, emit_p, end_p, corpus):
    inf = -float("inf")
    V = [{}]

    ## trans_p and emit_p preprocessing - co,pleteting missing probs-using smoothing or not
    for st in states:
        for prev_st in states:
            if st not in trans_p[prev_st]:
                trans_p[prev_st][st] = inf

    for st in states:
        if st not in start_p:
            start_p[st] = inf
        if st not in end_p:
            end_p[st] = inf
        for ob in obs:
            if ob not in emit_p[st]:
                emit_p[st][ob] = inf
            if 'UNK' not in emit_p[st]:
                emit_p[st]['UNK']=inf


        if obs[0] not in corpus:
            obs[0] = 'UNK'
        V[0][st] = {"prob": (start_p[st] + emit_p[st][obs[0]]), "prev": None}
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        if obs[t] not in corpus:
            obs[t] = 'UNK'
        V.append({})
        for st in states:
            max_tr_prob = max(V[t - 1][prev_st]["prob"] + trans_p[prev_st][st] for prev_st in states)
            for prev_st in states:
                if V[t - 1][prev_st]["prob"] + trans_p[prev_st][st] == max_tr_prob:
                    max_prob = max_tr_prob + emit_p[st][obs[t]]
                    if t == len(obs) - 1:
                        max_prob = max_tr_prob + emit_p[st][obs[t]] + end_p[st]
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break

    opt = []
    # The highest probability
    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    #print 'The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob
    return zip(obs, opt)
