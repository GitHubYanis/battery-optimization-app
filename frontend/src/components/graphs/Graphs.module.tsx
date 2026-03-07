import Plot from "react-plotly.js";
import type { ChartsResponse } from "../../interfaces/visualize-response";
import styles from './Graphs.module.css';

export function Graphs({ charts }: { charts: ChartsResponse }) {
    return (
        <div className={styles.graphsContainer}>
            {Object.values(charts).map((chart, index) => (
                <Plot key={index} data={chart.data} layout={chart.layout} />
            ))}
        </div>
    )
}