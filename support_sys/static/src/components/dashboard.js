/** @odoo-module */

import { registry } from "@web/core/registry";
import { KpiCard,CustomerCard } from "./kpi_card/kpi_card";
import { ChartRenderer } from "./chart_renderer/chart_renderer";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, useRef, onMounted, useState } = owl;
/*import { rpc } from "@web/core/web"*/

export class OwlReportingDashboard extends Component {
    async getMonthlySupport() {
        const domain = [['status', 'in', ['in_progress', 'new','closed']]];

        const filteredData = await this.orm.searchRead("support_sys.support_sys",domain, ['status', 'day_field'])
        const groupedData = {};
        filteredData.forEach(item => {
            const dayField = item.day_field.toString(); // Convert to string or use as required
            if (!groupedData[dayField]) {
                groupedData[dayField] = {
                    in_progress: 0,
                    new: 0,
                    closed:0
                // Add other status keys as needed
                };
            }

            if (item.status === 'in_progress') {
                groupedData[dayField].in_progress++;
            } else if (item.status === 'new') {
                groupedData[dayField].new++;
            } else if (item.status === 'closed') {
                groupedData[dayField].closed++;
            }
        // You can add more conditions for other status values if necessary
        });

        console.log(groupedData);

        this.state.getMonthlySupport = {
            data: {
                labels: Object.keys(groupedData),
                datasets: [
                    {
                        label: 'In Progress',
                        data: Object.values(groupedData).map(d => d.in_progress),
                        hoverOffset: 4
                    },
                    {
                        label: 'New',
                        data: Object.values(groupedData).map(d => d.new),
                        hoverOffset: 4
                    },
                    {
                        label: 'Closed',
                        data: Object.values(groupedData).map(d => d.closed),
                        hoverOffset: 4
                    }
                ]
            }
        };
    }


    setup() {
        this.state = owl.useState({
            problem: {
                value: 5,
                percentage:1,
                finished:1,
                fresh:1,
                progress:1,
            },
            /*distinctTicketTypes: [],*/
        });

        this.orm = useService("orm");

        onWillStart(async () => {
            await this.getTotalUsers();
            await this.getTotalClosedUsers();
            await this.getFreshNewUsers();
            await this.getTotalProgressUsers();
            await this.getMonthlySupport();


        });
    }

    async getTotalUsers() {
        try {
            const totalUsers = await this.orm.searchCount("support_sys.support_sys", [])
            this.state.problem.value = totalUsers;
            const today = new Date(); // Get today's date

            // Beginning of today
            const startOfToday = new Date(today);
            startOfToday.setHours(0, 0, 0, 0);

            // End of today (just before midnight)
            const endOfToday = new Date(today);
            endOfToday.setHours(23, 59, 59, 999);

            const todayFilter = [
            ['month_field', '>=', startOfToday.toISOString()],
            ['month_field', '<=', endOfToday.toISOString()]
            ];

            // Filter to count users created before today based on date_field
            const beforeTodayFilter = [
            ['month_field', '<', startOfToday.toISOString()]
            ];

            const yesterday = await this.orm.searchCount("support_sys.support_sys", beforeTodayFilter);
            const now =   await this.orm.searchCount("support_sys.support_sys", todayFilter);
            const rate = (((now - yesterday) / yesterday) * 10).toFixed(2);;
            this.state.problem.percentage = parseFloat(rate);

        } catch (error) {
        console.error("Error fetching total users:", error);
        }
    }
    async getTotalClosedUsers() {
        try {
            const domain = [['status', '=', 'closed']]; // Define domain to filter records
            const totalClosedUsers = await this.orm.searchCount("support_sys.support_sys", domain);
            this.state.problem.finished = totalClosedUsers;
        } catch (error) {
            console.error("Error fetching total closed users:", error);
        }
    }
    async getTotalProgressUsers() {
        try {
            const domain = [['status', '=', 'in_progress']]; // Define domain to filter records
            const totalClosedUsers = await this.orm.searchCount("support_sys.support_sys", domain);
            this.state.problem.progress = totalClosedUsers;
        } catch (error) {
            console.error("Error fetching total closed users:", error);
        }
    }
    async getFreshNewUsers() {
        try {
            const domain = [['ticket_type', '=', 'complain']]; // Define domain to filter records
            const totalClosedUsers = await this.orm.searchCount("ticket.raise", domain);
            this.state.problem.fresh = totalClosedUsers;
        } catch (error) {
            console.error("Error fetching total closed users:", error);
        }
    }
    /*async getTicketTypes() {
    try {
        const ticketTypes = await this.rpc({
            model: 'ticket.raise',
            method: 'search_read',
            args: [[]], // No domain to fetch all records
            kwargs: {
                fields: ['ticket_type'],
                groupBy: ['ticket_type'],
            },
        });

        const uniqueTicketTypes = ticketTypes.map(record => record.ticket_type);

        // Update the state with distinct ticket types
        this.state.distinctTicketTypes = uniqueTicketTypes;
    } catch (error) {
        console.error("Error fetching ticket types:", error);
    }*/
    /*for two array that we fetch have to combine and pass
    const combinedArray = this.state.distinctTicketTypes.concat(uniqueTicketTypes);

    */
}

OwlReportingDashboard.template = "owl.OwlReportingDashboard";
OwlReportingDashboard.components = { KpiCard, ChartRenderer,CustomerCard};

registry.category('actions').add('dashboard.owl.new.registry', OwlReportingDashboard);
