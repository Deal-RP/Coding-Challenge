from flask import Flask, request, Response, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/getFreeTime', methods = ['POST'])
def getFreeTime():
    data = request.get_json()
    if data:
        hOfficeInterval = getHInterval(data['hOffice'])
        hLunchInterval = getHInterval(data['hLunch'])
        freeMember = {}
        for i in range(hOfficeInterval[0], hOfficeInterval[1], data['tAverage']):
            if i < hLunchInterval[0] or i >= hLunchInterval[1]:
                nameList = []
                time = convertHourMinuteToString(i)
                for m in data['member']:
                    if time not in m['time']:
                        nameList.append(m['name'])
                if len(nameList) >= 3:
                    freeMember[time] = nameList

        return jsonify(
            freeMember = freeMember
        )
    return Response("Body not found",status=400,)

def getHInterval(interval):
    hInterval = interval.split("-")
    hResult = [convertHourStringToMinute(hInterval[0])]
    hResult.append(convertHourStringToMinute(hInterval[1]))
    return hResult

def convertHourStringToMinute(hour):
    stringFormat = "%I:%M%p" if ":" in hour else "%I%p"
    d = datetime.strptime(hour, stringFormat)
    hourMinute = d.strftime("%H:%M").split(":")
    return int(hourMinute[0]) * 60 + int(hourMinute[1])

def convertHourMinuteToString(minutes):
    stringFormat = "%I%p"
    hour = int(minutes) // 60
    formatAMPM = "PM" if hour - 12 >= 0 else "AM"
    hour = hour - 12 if hour - 12 > 0 else hour
    
    minutes = str(int(minutes) % 60)
    hourMinute = [str(hour)]
    if minutes != "0":
        stringFormat = "%I:%M%p"
        hourMinute.append(":")
        hourMinute.append(minutes)
    
    hourMinute.append(formatAMPM)
    
    d = datetime.strptime("".join(hourMinute), stringFormat)
    return d.strftime(stringFormat).lstrip('0')

if __name__ == '__main__':
   app.run(debug = True)