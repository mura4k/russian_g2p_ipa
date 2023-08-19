from russian_g2p.Transcription import Transcription
from typing import TypeVar


class Word:
    def __init__(self, transcription):
        self.transcription = transcription
        self.transcription_length = len(transcription)


Word_class_instance = TypeVar("Word_class_instance", bound=Word)


class Consonant:
    def __init__(self, consonant, index_in_word):
        self.consonant = consonant
        self.index_in_word = index_in_word


class TranscriptionIPA:
    def __init__(self):
        self.vowels = ['A0', 'O0', 'U0', 'Y0', 'E0', 'I0', 'A', 'O', 'U', 'Y', 'E', 'I']
        self.stressed_vowels = ['A0', 'O0', 'U0', 'Y0', 'E0', 'I0']

    def __put_stress_on_syllable(self, word: Word_class_instance) -> None:
        syllable_counter = 0
        sonority_levels = {
            'J0': 9, 'R': 8, 'R0': 8, 'L': 7, 'L0': 7,
            'M': 6, 'M0': 6, 'N': 6, 'N0': 6,
            'S': 5, 'S0': 5, 'SH': 5, 'SH0': 5, 'KH': 5, 'KH0': 5,  'GH': 5, 'GH0': 5,
            'V': 4, 'V0': 4, 'Z': 4, 'Z0': 4, 'ZH': 4, 'ZH0': 4,
            'F': 3, 'F0': 3,
            'B': 2, 'B0': 2, 'D': 2, 'D0': 2,  'G': 2, 'G0': 2,
            'P': 1, 'P0': 1, 'T': 1, 'T0': 1, 'K': 1, 'K0': 1,
            'TS': 0.5, 'TS0': 0.5, 'TSH': 0.5, 'TSH0': 0.5, 'DZ': 0.5, 'DZ0': 0.5, 'DZH': 0.5, 'DZH0': 0.5,

        }

        for sound_index, cur_sound in enumerate(word.transcription):
            if cur_sound in self.vowels:
                syllable_counter += 1

            if cur_sound in self.stressed_vowels:
                if syllable_counter == 1:
                    word.transcription.insert(0, 'ˈ')
                    break
                elif word.transcription[sound_index - 1] in self.vowels:
                    word.transcription.insert(sound_index, 'ˈ')
                    break
                else:
                    subword = []
                    subword_index = sound_index - 1

                    for sub_index in range(subword_index, -1, -1):
                        cur_sound = word.transcription[sub_index]
                        if cur_sound in self.vowels:
                            break
                        subword.append(Consonant(cur_sound, sub_index))

                    subword.reverse()

                    subword_len = len(subword)
                    if subword_len == 1:
                        word.transcription.insert(subword[0].index_in_word, 'ˈ')

                    else:
                        first_consonant = subword[0]
                        cur_sonority_level = sonority_levels[first_consonant.consonant]
                        for index in range(1, subword_len):
                            next_consonant = subword[index]
                            next_sonority_level = sonority_levels[next_consonant.consonant]

                            if cur_sonority_level <= next_sonority_level:
                                cur_sonority_level = next_sonority_level
                                if index == subword_len - 1:
                                    word.transcription.insert(first_consonant.index_in_word, 'ˈ')
                                    break

                            elif (cur_sonority_level >= 6 and next_sonority_level <= 5) or cur_sonority_level == 0.5:
                                word.transcription.insert(next_consonant.index_in_word, 'ˈ')
                                break

                            else:
                                word.transcription.insert(first_consonant.index_in_word, 'ˈ')
                                break

                    break

    def __translate_vowels(self, word: Word_class_instance) -> None:
        replace_vowel_pairs = {
            'U': 'u', 'U0': 'u', 'O0': 'o', 'A': 'a', 'A0': 'a', 'E0': 'e', 'I': 'i',
            'I0': 'i', 'Y': 'ɨ', 'Y0': 'ɨ'
        }
        for index, sound in enumerate(word.transcription):
            replacement = replace_vowel_pairs.get(sound)
            if replacement is not None:
                word.transcription[index] = replacement

    def __translate_consonants(self,  word: Word_class_instance) -> None:
        replace_consonant_pairs = {
            'P': 'p', 'P0': 'pʲ', 'B': 'b', 'B0': 'bʲ', 'T': 't', 'T0': 'tʲ',
            'D': 'd', 'D0': 'dʲ', 'K': 'k', 'K0': 'kʲ', 'G': 'ɡ', 'G0': 'ɡʲ',
            'TS': 't͡s', 'TS0': 't͡sʲ', 'TSH': 't͡ʃ', 'TSH0': 't͡ʃʲ', 'DZ': 'ʣ',
            'DZ0': 'ʣʲ', 'DZH': 'dʒ', 'DZH0': 'dʒʲ', 'KH': 'x', 'KH0': 'xʲ',
            'SH': 'ʃ', 'SH0': 'ʃʲː', 'ZH': 'ʒ', 'ZH0': 'ʒʲː', 'GH': 'ɣ',
            'GH0': 'ɣʲ', 'F': 'f', 'F0': 'fʲ', 'V': 'v', 'V0': 'vʲ', 'S': 's',
            'S0': 'sʲ', 'Z': 'z', 'Z0': 'zʲ',
            'M': 'm', 'M0': 'mʲ', 'N': 'n', 'N0': 'nʲ', 'L': 'l', 'L0': 'lʲ',
            'J0': 'j', 'R': 'r', 'R0': 'rʲ'
        }

        for index, sound in enumerate(word.transcription):
            replacement = replace_consonant_pairs.get(sound)
            if replacement is not None:
                word.transcription[index] = replacement

    def __format_output(self, transcription: list) -> str:
        result = []

        for phrase in transcription:
            if phrase:
                word_parts = []
                for word in phrase:
                    word_parts.append(''.join(word))
                result.append('/' + ' '.join(word_parts) + '/')

        if result:
            return ', '.join(result)
        else:
            return ''

    def transcribe(self, texts: list):
        transcriptor = Transcription()
        orthographic_transcription = transcriptor.transcribe(texts, ipa=True)
        for g2p_phrase in orthographic_transcription:
            for g2p_word in g2p_phrase:
                word = Word(g2p_word)
                self.__put_stress_on_syllable(word)
                self.__translate_vowels(word)
                self.__translate_consonants(word)
        result = self.__format_output(orthographic_transcription)
        return result
