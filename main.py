from Spartacus import Spartacus, audio_out, audio_in

# todo -- test more, code is scrappy af

s = Spartacus()

# s.query_search_engines_FF('price of a computer')

query_statement = audio_in()
query_response = s.query_search_engines_FF(query_statement)
audio_out(query_response)