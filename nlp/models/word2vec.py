from collections import Counter
from typing import Iterator, List, Tuple, Any
import tqdm

SentenceIterator = Iterator[List[str]]
TextIterator = Iterator[Tuple[Any, SentenceIterator]]

# _unk_, _bos_, _eos_, _upp_, _maj_
NUM_OF_SPECIAL_TOKENS = 5


class Vocabulary:
    def __init__(self, gen: TextIterator=None, counts: Counter=None):
        if gen is not None:
            self.counts = Vocabulary._create_vocabulary(gen)
        elif counts is not None:
            self.counts = counts
        else:
            raise Exception("Either sentence generator or \
                token counts must be supplied!")

        self.tokens, self.token_index, self.index_token = \
            Vocabulary._indices_from_counts(self.counts)

    @staticmethod
    def _indices_from_counts(counts: Counter):
        tokens = [w for w, c in counts.most_common()]
        token_index = dict(zip(
            tokens,
            range(NUM_OF_SPECIAL_TOKENS, NUM_OF_SPECIAL_TOKENS + len(tokens))))
        token_index["_unk_"] = 0
        token_index["_bos_"] = 1
        token_index["_upp_"] = 2
        token_index["_maj_"] = 3
        token_index["_eos_"] = 4
        index_token = dict([(ind, w) for w, ind in token_index.items()])

        return tokens, token_index, index_token

    @staticmethod
    def _create_vocabulary(gen: TextIterator) -> Counter:
        cnt = Counter()
        for _, text in tqdm.tqdm(gen):
            for sent in text:
                for token in sent:
                    cnt[token.lower()] += 1

        return cnt

    def prune_vocabulary(self, min_count=1):
        counts = Counter(dict([
            (w, c) for w, c in self.counts.items() if c >= min_count]))
        return Vocabulary(counts=counts)


def encode_sentence(s: List[str], vocab) -> List[int]:

    es = []
    es.append("_bos_")
    for token in s:
        if token.istitle():
            es.append("_maj_")
        elif token.isupper():
            es.append("_up_")
        token = token.lower()
        if vocab[token]:
            es.append(token)
        else:
            es.append("_unk_")

    es.append("_eos_")
    return es


# def cbow_tf_records(s: List[str]) -> List[tf.TFRecord])???
