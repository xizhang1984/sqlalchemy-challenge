{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func\n",
    "\n",
    "from flask import Flask, jsonify\n",
    "import datetime as dt\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "engine = create_engine(\"sqlite:///Resources/hawaii.sqlite\")\n",
    "\n",
    "\n",
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "# reflect the tables\n",
    "Base.prepare(engine, reflect=True)\n",
    "\n",
    "# Save references to each table\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station\n",
    "session = Session(engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Flask Setup\n",
    "app = Flask(__name__)\n",
    "\n",
    "# Flask Routes\n",
    "@app.route(\"/\")\n",
    "def welcome():\n",
    "    return (\n",
    "        f\"Welcome to the sqlalchemy API!<br/>\"\n",
    "        f\"Available Routes:<br/>\"\n",
    "        f\"/api/v1.0/precipitation<br/>\"\n",
    "        f\"/api/v1.0/stations<br/>\"\n",
    "        f\"/api/v1.0/tobs<br/>\"\n",
    "        f\"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>\"\n",
    "        f\"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>\"\n",
    "    )"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def precipitation():\n",
    "    # Create our session (link) from Python to the DB\n",
    "    session = Session(engine)\n",
    "\n",
    "    \"\"\"Return a list of all Precipitation Data\"\"\"\n",
    "    # Query all Precipitation\n",
    "    results = session.query(Measurement.date,Measurement.prcp).\\\n",
    "                order_by(Measurement.date).all()\n",
    "\n",
    "    session.close()\n",
    "\n",
    "\n",
    "    # Convert list of tuples into normal list\n",
    "    all_precipitation = list(np.ravel(results))\n",
    "    \n",
    "    # Convert the list to Dictionary\n",
    "    all_precipitation = {all_precipitation[i]: all_precipitation[i + 1] for i in range(0, len(all_precipitation), 2)} \n",
    "\n",
    "    return jsonify(all_precipitation)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "    # Create our session (link) from Python to the DB\n",
    "    session = Session(engine)\n",
    "\n",
    "    \"\"\"Return a list of all Stations\"\"\"\n",
    "    # Query all Stations\n",
    "    results = session.query(Station.station).\\\n",
    "                 order_by(Station.station).all()\n",
    "\n",
    "    session.close()\n",
    "\n",
    "    # Convert list of tuples into normal list\n",
    "    all_stations = list(np.ravel(results))\n",
    "\n",
    "    return jsonify(all_stations)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tobs():\n",
    "     # Create our session (link) from Python to the DB\n",
    "    session = Session(engine)\n",
    "\n",
    "    \"\"\"Return a list of all TOBs\"\"\"\n",
    "    # Query all tobs\n",
    "\n",
    "    results = session.query(Measurement.date,  Measurement.tobs).\\\n",
    "                filter(Measurement.date >= '2016-08-23').\\\n",
    "                    order_by(Measurement.date).all()\n",
    "\n",
    "    session.close()\n",
    "\n",
    "    # Convert list of tuples into normal list\n",
    "    all_tobs = list(np.ravel(results))\n",
    "\n",
    "    # Convert the list to Dictionary\n",
    "    all_tobs = {all_tobs[i]: all_tobs[i + 1] for i in range(0, len(all_tobs), 2)} \n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "@app.route(\"/api/v1.0/temp/<start>\")\n",
    "def data_start_date(start_date):\n",
    "    # Create our session (link) from Python to the DB\n",
    "    session = Session(engine)\n",
    "\n",
    "    \"\"\"Return a list of min, avg and max tobs for an specific start date\"\"\"\n",
    "    # Query all tobs\n",
    "\n",
    "    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\\\n",
    "                filter(Measurement.date >= start_date).all()\n",
    "\n",
    "    session.close()\n",
    "\n",
    "    # Alternative 1\n",
    "    # Convert list of tuples into normal list\n",
    "    # start_date_tobs = list(np.ravel(results))\n",
    "    \n",
    "    # Create a dictionary from the row data and append to a list of start_date_tobs\n",
    "    start_date_tobs = []\n",
    "    for min, avg, max in results:\n",
    "        start_date_tobs_dict = {}\n",
    "        start_date_tobs_dict[\"min_temp\"] = min\n",
    "        start_date_tobs_dict[\"avg_temp\"] = avg\n",
    "        start_date_tobs_dict[\"max_temp\"] = max\n",
    "        start_date_tobs.append(start_date_tobs_dict) \n",
    "    \n",
    "    \n",
    "    \n",
    "    return jsonify(start_date_tobs)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/temp/<start>/<end>\")\n",
    "def data_start_end_date(start_date, end_date):\n",
    "    # Create our session (link) from Python to the DB\n",
    "    session = Session(engine)\n",
    "\n",
    "    \"\"\"Return a list of min, avg and max tobs for an specific start and end dates\"\"\"\n",
    "    # Query all tobs\n",
    "\n",
    "    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\\\n",
    "                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()\n",
    "\n",
    "    session.close()\n",
    "\n",
    "    # Alternative 1\n",
    "    # Convert list of tuples into normal list\n",
    "    # start_end_date_tobs = list(np.ravel(results))\n",
    "    \n",
    "    # Create a dictionary from the row data and append to a list of start_end_date_tobs\n",
    "    start_end_date_tobs = []\n",
    "    for min, avg, max in results:\n",
    "        start_end_date_tobs_dict = {}\n",
    "        start_end_date_tobs_dict[\"min_temp\"] = min\n",
    "        start_end_date_tobs_dict[\"avg_temp\"] = avg\n",
    "        start_end_date_tobs_dict[\"max_temp\"] = max\n",
    "        start_end_date_tobs.append(start_end_date_tobs_dict) \n",
    "    \n",
    "\n",
    "    return jsonify(start_end_date_tobs)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: This is a development server. Do not use it in a production deployment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Restarting with windowsapi reloader\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\u001b[1;31m:\u001b[0m 1\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\xzhan\\anaconda3\\lib\\site-packages\\IPython\\core\\interactiveshell.py:3339: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.\n",
      "  warn(\"To exit: use 'exit', 'quit', or Ctrl-D.\", stacklevel=1)\n"
     ]
    }
   ],
   "source": [
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
