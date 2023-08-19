import unittest

from russian_g2p.TranscriptionIPA import TranscriptionIPA


class TestAll(unittest.TestCase):
    def setUp(self):
        self.__transcriptionIPA = TranscriptionIPA()

    def tearDown(self):
        del self.__transcriptionIPA

    def test_normal(self):
        source_phrase = ['Мама мыла раму']
        target_variants = '/ˈmama ˈmɨla ˈramu/'
        real_variants = self.__transcriptionIPA.transcribe(source_phrase)
        self.assertEqual(target_variants, real_variants)

    def test_symbols(self):
        source_phrase = ['Мама мыла ра-му, а ты?! - Нет.']
        target_variants = '/ˈmama ˈmɨla ˈra ˈmu a ˈtɨ ˈnʲet/'
        real_variants = self.__transcriptionIPA.transcribe(source_phrase)
        self.assertEqual(target_variants, real_variants)

    def test_nothing(self):
        source_phrase = ['...']
        target_variants = ''
        real_variants = self.__transcriptionIPA.transcribe(source_phrase)
        self.assertEqual(target_variants, real_variants)

    def test_syllable_accent(self):
        source_phrase = ['воскликнуть', 'подставка', 'конструкция', 'волна+', 'обзор', 'правление', 'проклятие',
                         'усомниться', 'подлец', 'подостлать', 'сполна+', 'пастель', 'чайка+', 'балкон', 'мальчи+шка']
        target_variants = '/vaˈsklʲiknutʲ/, /paˈt͡stafka/, /kanˈstrukt͡sɨja/, /vaˈlna/, /aˈbzor/, /praˈvlʲenʲiji/, ' \
                          '/praˈklʲatʲiji/, /usaˈmnʲit͡sa/, /paˈdlʲet͡s/, /padaˈslatʲ/, /spaˈlna/, /paˈsʲtʲelʲ/, ' \
                          '/t͡ʃʲijˈka/, /balˈkon/, /malʲˈt͡ʃʲiʃka/'
        real_variants = self.__transcriptionIPA.transcribe(source_phrase)
        self.assertEqual(target_variants, real_variants)


if __name__ == '__main__':
    unittest.main(verbosity=2)
