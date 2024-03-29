import {Box, CircularProgress, useTheme} from "@mui/material";
import {DataGrid} from "@mui/x-data-grid";
import {tokens} from "../../theme";
import React, {useState, useEffect} from "react";
import config from "../../config.json";
import axios from "axios";
import Topbar from "../global/Topbar";

const TransactionHistory = () => {
    const [transactions, setTransactions] = useState([]);
    const [isLoading, setIsLoading] = useState(true)

    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    useEffect(() => {
        getTransactions()
    }, []);

    const getTransactions = async () => {
        try{
            const response = await axios.get(`${config.url}/transactions`, {
                headers: {
                    Authorization: JSON.parse(localStorage.getItem("user")).token,
                },
            });
            setTransactions(response.data)
            console.log(response.data)
            setIsLoading(false)
        } catch(error){
            console.log(error)
            setIsLoading(false)
        }
    }
    const getRowClassName = (params) => {
        if (params.row.is_buy === 'sell') {
            return 'sell-row';
        }
        else {
            return 'buy-row';
        }
    };
    const columns = [
        {field: "id", headerName: "Id", width:30},
        {field: "ticker", headerName: "ticker", width:120},
        {
            field: "piece_price",
            headerName: "Price per piece",
            flex: 1,
            width:150
        },
        {
            field: "total_price",
            headerName: "Total Price",
            flex: 1,
            width:150
        },

        {
            field: "quantity",
            headerName: "Quantity",
            flex: 1,
            width:50

        },
        {
            field: "date",
            headerName: "Date",
            flex: 1,
            width:200
        },
        {
            field: "is_buy",
            headerName: "Type",
            flex: 1,
            width:100
        }
    ];

    return (
        <Box m="20px">
            <Topbar title="TRANSACTION HISTORY" subtitle="Get through the history of your transactions" ticker={'transactionHistory'} isTicker={false}/>
            { !isLoading ? (<Box
                height="75vh"
                sx={{
                    "& .MuiDataGrid-root": {
                        border: "none",
                    },
                    "& .MuiDataGrid-cell": {
                        borderBottom: "none",
                        fontSize: "15px"
                    },
                    "& .name-column--cell": {
                        color: colors.greenAccent[300],
                    },
                    "& .MuiDataGrid-columnHeaders": {
                        backgroundColor: colors.blueAccent[700],
                        borderBottom: "none",
                        fontSize: "15px"
                    },
                    "& .MuiDataGrid-virtualScroller": {
                        backgroundColor: colors.primary[400]
                    },
                    "& .MuiDataGrid-footerContainer": {
                        borderTop: "none",
                        backgroundColor: colors.blueAccent[700],
                        fontSize: "15px"
                    },
                    "& .MuiCheckbox-root": {
                        color: `${colors.greenAccent[200]} !important`,
                    },
                    ".buy-row": {color: colors.greenAccent[500]},
                    ".sell-row": {color: colors.redAccent[500]}
                }}
            >
                <DataGrid rows={transactions} columns={columns} getRowClassName={getRowClassName}/>
            </Box>):(
            <Box sx={{ display: 'flex', justifyContent:"center", alignItems:"center", height:"70vh"}}>
                <CircularProgress sx={{color: colors.primary[300]}} />
            </Box>
            )}
        </Box>
    );
};

export default TransactionHistory;
