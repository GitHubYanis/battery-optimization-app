import type { VisualizeSummary } from '../../interfaces/visualize-response';
import styles from './Summary.module.css'

export function Summary({ summary }: { summary: VisualizeSummary }) {
    return (
        <div className={styles.summaryContainer}>
            <p className={styles.summaryTitle}>Résumé des résultats: </p>
            <table className={styles.summaryTable}>
              <thead>
                <tr>
                  <th></th>
                  <th>Avant</th>
                  <th>Après</th>
                  <th>Économie/Gain</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Coût total</td>
                  <td>${summary.total_cost_before.toFixed(2)}</td>
                  <td>${summary.total_cost_after.toFixed(2)}</td>
                  <td className={styles.savings}>${summary.savings.toFixed(2)}</td>
                </tr>
                <tr>
                  <td>Puissance maximale</td>
                  <td>{summary.peak_before_kw.toFixed(2)} kW</td>
                  <td>{summary.peak_after_kw.toFixed(2)} kW</td>
                  <td className={styles.savings}>{Math.abs(summary.peak_before_kw - summary.peak_after_kw).toFixed(2)} kW</td>
                </tr>
              </tbody>
            </table>
        </div>
    )
}