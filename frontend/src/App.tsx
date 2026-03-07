import { useEffect, useState } from 'react';
import './App.css'
import { MOCK_DATA, API_URL, API_KEY } from './constants';
import type { VisualizeResponse } from './interfaces/visualize-response';
import { Summary } from './components/summary/Summary.module';
import { Graphs } from './components/graphs/Graphs.module';


function App() {
  const [data, setData] = useState<VisualizeResponse | null>(null);

  useEffect(() => {
    fetch(`${API_URL}/visualize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY,
      },
      body: JSON.stringify({
        load_kwh: MOCK_DATA.load,
        price_per_kwh: MOCK_DATA.prices,
        battery: MOCK_DATA.battery,
      }),
    })
    .then(response => response.json())
    .then((data: VisualizeResponse) => setData(data))
    .catch(error => {
      console.error('Error fetching optimization results:', error);
    });
  }, []);

  return (
    <>
      <h1 className='results-title'>Optimisation de Batterie</h1>
      {data ? (
        <>
          <Summary summary={data.summary} />
          <Graphs charts={data.charts} />
        </>
        ) : (<p>Chargement des résultats d'optimisation...</p>
        )}
    </>
  )
}

export default App
