/** @odoo-module */

import { registry } from "@web/core/registry"
import { loadJS } from "@web/core/assets"
const { Component, onWillStart, useRef, onMounted } = owl
/*import { rpc } from "@web/core/web"*/

export class ChartRenderer extends Component {

    setup(){
        this.chartRef = useRef("chart")
        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js")
           /* await this.fetchChartData()*/
        })

        onMounted(()=>this.renderChart())
    }
   /* async fetchChartData() {
        try {
            const data = await rpc.query({
                model: 'support_sys.support_sys',
                method: 'fetch_data',
                args: [],
            });

            console.log('Fetched Data:', data);

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }*/
    renderChart(){
        new Chart(this.chartRef.el,
        {
          type: this.props.type,
          data: this.props.config.data,
          /*{
            labels: [
                'September',
                'October',
                'November'
              ],
              datasets: [
              {
                label: 'Problem Solved',
                data: [300, 50, 100],
                hoverOffset: 4
              },{
                label: 'Problem Raised',
                data: [100, 70, 150],
                hoverOffset: 4
              }]
          }*/
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'bottom',
              },
              title: {
                display: true,
                text: this.props.title,
                position: 'bottom',
              }
            }
          },
        }
      );
    }
}

ChartRenderer.template = "owl.ChartRenderer"