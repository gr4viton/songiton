import simplejson
import requests


class Invoker:
    def invoke(self, fname):
        plaintext = self.load_file(fname)
        self.get_song_from_plaintext(plaintext)

    def get_song_from_plaintext(self, plaintext):
        base_url = "http://127.0.0.1:8000"
        full_path = f"{base_url}/song/from_plaintext"
        full_path = "http://127.0.0.1:8000/song/from-plaintext"

        data = plaintext.encode("utf-8")
        request_json = {"plaintext": data}
        respo = requests.put(full_path, json=request_json)
        response_txt = respo.text
        if respo.text:
            print("respo_text")
            try:
                ensure_ascii = False
                ftext = simplejson.dumps(simplejson.loads(response_txt), indent=2, ensure_ascii=ensure_ascii)
            except:
                ftext = respo.text
            print(ftext)

        if not respo.ok:
            print("NOK")
            print(respo.status_code)
            return

    def load_file(self, fname):
        with open(fname, "r") as fil:
            plaintext = fil.read()
        return plaintext


if __name__ == "__main__":
    invo = Invoker()
    fname = "to_convert/plaintext/noha_v_dumku.lorem.txt"
    invo.invoke(fname)
