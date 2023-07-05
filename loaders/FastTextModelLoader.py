import fasttext


class FastTextModelLoader:
    _fast_text_model = None

    @staticmethod
    def get_fast_text_model():
        if FastTextModelLoader._fast_text_model is None:
            FastTextModelLoader._fast_text_model = fasttext.load_model('models/model300d.bin')
            return FastTextModelLoader._fast_text_model
        else:
            return FastTextModelLoader._fast_text_model
