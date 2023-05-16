import {CircularProgress, useTheme} from "@mui/material";
import {ResponsiveBar} from "@nivo/bar";
import {tokens} from "../theme";
import React, {useEffect, useState} from "react";
import axios from "axios";
import config from "../config.json";

const RevenueBarChart = ({stock_name}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [chartJson, setChartJson] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState({});

    useEffect(() => {
        getRevenueChart()
    }, []);
    const getRevenueChart = async () => {
        try {
            const response = await axios.get(`${config.url}/stock/chart/revenue/${stock_name}`);
            setChartJson(response.data)
            setError("")
            setIsLoading(false)
        } catch (error) {
            console.log(error)
            setError("Failed to get price chart!")
            setIsLoading(false)
        }
    }

    if (isLoading) {
      return (
          <div style={{display: 'flex', justifyContent: 'center'}}>
            <CircularProgress status="loading" />
          </div>
      );
    }

    return (
            <ResponsiveBar
                data={chartJson}
                keys={[
                    "color1","color2","color3","MillionsRevenue"
                ]}
                indexBy="quarter"
                margin={{top: 50, right: 130, bottom: 50, left: 60}}
                padding={0.3}
                valueScale={{type: 'linear'}}
                indexScale={{type: 'band', round: true}}
                colors={{scheme: 'greens'}}
                defs={[
                    {
                        id: 'dots',
                        type: 'patternDots',
                        background: 'inherit',
                        color: 'red',
                        size: 4,
                        padding: 1,
                        stagger: true
                    },
                    {
                        id: 'lines',
                        type: 'patternLines',
                        background: 'inherit',
                        color: 'red',
                        rotation: -45,
                        lineWidth: 6,
                        spacing: 10
                    }
                ]}
                borderColor={{
                    from: 'color',
                    modifiers: [
                        [
                            'darker',
                            3
                        ]
                    ]
                }}
                axisTop={null}
                axisRight={null}
                axisBottom={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: -20,
                    legend: 'quarter',
                    legendPosition: 'middle',
                    legendOffset: 40,
                }}
                axisLeft={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    legend: 'Revenue in Million$',
                    legendPosition: 'middle',
                    legendOffset: -53
                }}
                theme={{
                    // added
                    axis: {
                        domain: {
                            line: {
                                stroke: colors.grey[100],
                            },
                        },
                        legend: {
                            text: {
                                fill: colors.grey[100],
                            },
                        },
                        ticks: {
                            line: {
                                stroke: colors.grey[100],
                                strokeWidth: 1,
                            },
                            text: {
                                fill: colors.grey[100],
                            },
                        },
                    },
                    legends: {
                        text: {
                            fill: colors.grey[100],
                        },
                    },
                    tooltip: {
                        container: {
                            color: colors.grey[900],
                        },
                    },

                }}
                labelSkipWidth={12}
                labelSkipHeight={12}
                labelTextColor={{
                    from: 'color',
                    modifiers: [
                        [
                            'darker',
                            0
                        ]
                    ]
                }}
                role="application"
                ariaLabel="Nivo bar chart demo"
                barAriaLabel={e => e.id + ": " + e.formattedValue + " in country: " + e.indexValue}
            />
    );
};

export default RevenueBarChart;