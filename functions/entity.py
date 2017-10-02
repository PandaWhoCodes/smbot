import nltk


class extractor():
    chunked_sentences = []

    def __init__(self, s):
        """
        initializing the class with the sentence which will be tokenized and chuncked
        """
        sentences = nltk.sent_tokenize(s)
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
        chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
        self.chunked_sentences = chunked_sentences

    def extract_entity_names(self, t):
        """
        Returns extracted entities
        :param t: nltk tree
        :return: entity list
        """
        entity_names = []
        for i in t:
            if "NE" in str(i) or "NN" in str(i) or "NNE" in str(i) or "NNP" in str(i) or "JJ" in str(i) or "VBP" in str(
                    i):
                if str(type(i[0])) == "<class 'tuple'>":
                    entity_names.append(str(i[0][0]))
                else:
                    entity_names.append(str(i[0]))
        return entity_names

    def extract(self):
        """
        A helper function for extract_entity_names
        :return: Entity list
        """
        entity_names = []
        entity_names1 = []
        for tree in self.chunked_sentences:
            entity_names.extend(self.extract_entity_names(tree))
        for entities in entity_names:
            entity_names1.append(entities.lower())
        return entity_names1
