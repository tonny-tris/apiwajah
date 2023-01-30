from fastapi.staticfiles import StaticFiles
from gtts import gTTS
import uuid
from skimage import io
from fastapi import FastAPI, Request, Response, status, Body
from fastapi.middleware.cors import CORSMiddleware
import cv2
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.mount("/filemp3", StaticFiles(directory="filemp3"), name="filemp3")


@app.get("/")
async def root():
    return {"message": "Terhubung Python 3.7 DisKominfo"}

@app.post("/tts", status_code=200)
async def getInformation(info: Request, response: Response):
  req = await info.json()
  # text = 'Selamat Datang Di API Python'
  text = req['text']
  language = 'id'
  objek = gTTS(text=text, lang=language, slow=False)
  acak = str(uuid.uuid4())
  namafile = acak + ".mp3"
  objek.save("./filemp3/" + namafile)
  # os.system("start ./filemp3/" + namafile)
  response.status_code = status.HTTP_200_OK
  return {
    "metadata": {
        "code": 200,
        "status": "OK",
        "message": "Berhasil Text To Speech"
    },
    "response": {
        "urlmp3": "http://103.161.108.40:8000/filemp3/" + namafile
    }
  }

@app.options("/detectwajah", status_code=200)
async def main(info: Request):
  req = await info.json()
  # return req
  faceCascade = cv2.CascadeClassifier("C:/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml")
  array = []
  arraywajahmasuk = []
  arraywajahpulang = []
  for idx, x in enumerate(req) :
      if x['fmurl'] == '' :
          arraywajahmasuk.append("Tidak Ditemukan Wajah")
      else :
          try :
              gambarmasuk = io.imread(x['fmurl'])
              abumasuk = cv2.cvtColor(gambarmasuk, cv2.COLOR_BGR2GRAY)
              wajahmasuk = faceCascade.detectMultiScale(abumasuk)
              if len(wajahmasuk) == 1:
                  arraywajahmasuk.append("Ditemukan Wajah")
              else:
                  arraywajahmasuk.append("Tidak Ditemukan Wajah")
          except :
              arraywajahmasuk.append("Tidak Ditemukan Wajah")
      if x['fpurl'] == '' :
          arraywajahpulang.append("Tidak Ditemukan Wajah")
      else :
          try :
              gambarpulang = io.imread(x['fpurl'])
              abupulang = cv2.cvtColor(gambarpulang, cv2.COLOR_BGR2GRAY)
              wajahpulang = faceCascade.detectMultiScale(abupulang)
              if len(wajahpulang) == 1:
                  arraywajahpulang.append("Ditemukan Wajah")
              else:
                  arraywajahpulang.append("Tidak Ditemukan Wajah")
          except :
              arraywajahpulang.append(0)
      array.append({'id': x['id'], 'hari': x['hari'], 'nama': x['nama'], 'jammasuk': x['jammasuk'], 'jenismasuk': x['jenismasuk'], 'fotomasuk': x['fotomasuk'], 'wajahmasuk': arraywajahmasuk[idx] ,'jampulang': x['jampulang'], 'jenispulang': x['jenispulang'], 'fotopulang': x['fotopulang'], 'wajahpulang': arraywajahpulang[idx]})
  return {
      "metadata": {
          "code": 200,
          "status": "OK",
          "message": "Berhasil Detect Wajah"
      },
      "response": {
          "data": array
      }
  }

@app.options("/deteksiwajah", status_code=200)
async def main(info: Request, response: Response):
    req = await info.json()
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = io.imread(req['foto'])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0:
        response.status_code = status.HTTP_200_OK
        return {
            "metadata": {
                "code": 200,
                "status": "OK",
                "message": "Berhasil Detect Wajah"
            },
            "response": {
                "data": "Ditemukan wajah"
            }
        }
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "metadata": {
                "code": 404,
                "status": "NOT FOUND",
                "message": "Gagal Detect Wajah"
            },
            "response": {
                "data": "Tidak Ditemukan wajah"
            }
        }

