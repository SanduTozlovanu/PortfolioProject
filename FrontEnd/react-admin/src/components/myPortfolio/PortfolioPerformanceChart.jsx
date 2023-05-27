import React, {useEffect, useState} from 'react';
import Plotly from 'plotly.js-basic-dist';
import createPlotlyComponent from 'react-plotly.js/factory';
import axios from "axios";
import config from "../../config.json";
import {Box, CircularProgress, Typography, useTheme} from "@mui/material";
import {tokens} from "../../theme";

const Plot = createPlotlyComponent(Plotly);
const PortfolioPerformanceChart = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [chartJson, setChartJson] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState({});

    useEffect(() => {
        getPortoflioPerformanceChart()
    }, []);
    const getPortoflioPerformanceChart = async () => {
        try {
            const response = await axios.get(`${config.url}/portfolio/chart/performance`, {
                headers: {
                    Authorization: JSON.parse(localStorage.getItem("user")).token,
                },
            });
            setChartJson(response.data)
            setError("")
            setIsLoading(false)
        } catch (error) {
            console.log(error)
            setError("Failed to get portfolio performance chart!")
            setIsLoading(false)
        }
    }
    if (isLoading) {
        return (
            <Box sx={{ display: 'flex', justifyContent:"center", alignItems:"center", height:"50vh"}}>
                <CircularProgress sx={{color: colors.primary[300]}} />
            </Box>
        );
    }

    return (
        <Box marginLeft={-1} marginTop={1}>
            <Typography variant="h3" style={{ textAlign: 'center' }}>Portfolio Performance</Typography>
            <Plot useResizeHandler={true}
                data={chartJson.data.map(data => ({
                    ...data,
                    marker: {
                        ...data.marker,
                        color: colors.greenAccent[500], // Set marker color to blue
                    },
                    line: {
                        ...data.line,
                        color: colors.greenAccent[500], // Set line color to blue
                    },
                    fill: 'tozeroy', // Enable fill under the markers
                }))}
                layout={{
                    ...chartJson.layout,
                    margin: {
                        ...chartJson.layout.margin,
                        t: 40,
                        l: 0
                    },
                    xaxis: {
                        ...chartJson.layout.xaxis,
                        type: 'date', // Set x-axis type to date
                        tickfont: {
                            color: 'white', // Change x-axis tick color to white
                        },
                    },
                    yaxis: {
                        ...chartJson.layout.yaxis,
                        range: [Math.min(...chartJson.data[0].y), Math.max(...chartJson.data[0].y)], // Set y-axis range based on data
                        tickfont: {
                            color: 'white', // Change x-axis tick color to white
                        },
                    },
                    plot_bgcolor: colors.grey[0], // Set plot background color
                    paper_bgcolor: colors.primary[500], // Set paper background color
                    autosize: true
                }} style={{width: "100%", height: "100%"}}
            />
        </Box>
    );
};

export default PortfolioPerformanceChart;