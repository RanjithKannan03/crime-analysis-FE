import React, { useState } from 'react';
import axios from 'axios';

const CrimePredictionForm = () => {
  const [formData, setFormData] = useState({
    Location: '',
    Time_of_Day: '',
    Weather: '',
    Demographics: ''
  });

  const [responsePlan, setResponsePlan] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const predictionResponse = await axios.post('http://127.0.0.5000/predict_crime', formData);
      const crimePrediction = predictionResponse.data.crime_prediction;

      const responsePlanResponse = await axios.post('http://127.0.0.5000/suggest_response_plan', {
        ...formData,
        crime_type: crimePrediction
      });
      setResponsePlan(responsePlanResponse.data.response_plan);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Location:
          <input type="text" name="Location" value={formData.Location} onChange={handleChange} />
        </label>
        <label>
          Time of Day:
          <input type="text" name="Time_of_Day" value={formData.Time_of_Day} onChange={handleChange} />
        </label>
        <label>
          Weather:
          <input type="text" name="Weather" value={formData.Weather} onChange={handleChange} />
        </label>
        <label>
          Demographics:
          <input type="text" name="Demographics" value={formData.Demographics} onChange={handleChange} />
        </label>
        <button type="submit">Predict Crime</button>
      </form>
      {responsePlan && (
        <div>
          <h2>Response Plan:</h2>
          <p>{responsePlan}</p>
        </div>
      )}
    </div>
  );
};

export default CrimePredictionForm;
