import {Box, Typography, IconButton, FormHelperText, useTheme} from "@mui/material";
import {DataGrid} from "@mui/x-data-grid";
import {tokens} from "../../theme";
import {stockScreenerFilters} from "../../data/mockData";
import { useNavigate } from 'react-router-dom';
import Select from "../../components/SelectComponent";
import {useState, useEffect} from "react";
import SearchIcon from '@mui/icons-material/Search';
import config from "../../config.json";
import axios from "axios";
import InputBase from "@mui/material/InputBase";
import Topbar from "../global/Topbar";

const StockScreener = () => {
    const [stocks, setStocks] = useState([]);
    const [error, setError] = useState('');
    const [marketCapRange, setMarketCapRange] = useState("");
    const [priceRange, setPriceRange] = useState("");
    const [betaRange, setBetaRange] = useState("");
    const [volumeRange, setVolumeRange] = useState("");
    const [dividendRange, setDividendRange] = useState("");
    const [sector, setSector] = useState("");
    const [selectedStock, setSelectedStock] = useState("");

    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();

    useEffect(() => {
        search()
    }, [marketCapRange, priceRange, betaRange, volumeRange, dividendRange, sector]);

    const handleInputChange = (event) => {
        setSelectedStock(event.target.value);
    };
    const rowClickEvent = (params) => {
        console.log("stockProfile ticker " + stocks[params.id - 1].ticker)
        navigate('/stockProfile/' + stocks[params.id - 1].ticker)
    }

    const search = async () => {
        let queryParams = composeQueryParams()
        console.log(queryParams)

        try{
            const response = await axios.get(`${config.url}/stock/search${queryParams}`);
            setStocks(response.data)
            setError("")
        } catch(error){
            console.log(error)
            setError("Failed to get search stocks!")
        }
    }
    const searchStock = async () => {
        if (selectedStock === "")
            return
        try{
            const response = await axios.get(`${config.url}/stock/search/${selectedStock}`);
            setStocks(response.data)
            setError("")
        } catch(error){
            console.log(error)
            setError("Failed to get search stocks!")
        }
    }
    const composeQueryParams = () => {
        let queryParams = "?"
        queryParams = composeQueryParam(queryParams, marketCapRange)
        queryParams = composeQueryParam(queryParams, priceRange)
        queryParams = composeQueryParam(queryParams, betaRange)
        queryParams = composeQueryParam(queryParams, volumeRange)
        queryParams = composeQueryParam(queryParams, dividendRange)
        if (sector)
        {
            queryParams = composeQueryParam(queryParams, `sector=${sector}`)

        }
        return queryParams

    }
    const composeQueryParam = (params, param) => {
        if (params === "?" && param)
        {
            params += param
        }
        else if(params !== "?" && param)
        {
            params += "&"
            params += param
        }
        return params

    }
    const columns = [
        {field: "id", headerName: "Id", width:30},
        {field: "name", headerName: "Name", width:200},
        {
            field: "price",
            headerName: "Price",
            flex: 1,
            width:50,
            renderCell: (params) => (
                <Typography color={colors.greenAccent[500]}>
                    ${params.row.price}
                </Typography>
            )
        },
        {
            field: "marketCap",
            headerName: "Market Cap",
            flex: 1,
            width:100,
            renderCell: (params) => (
                <Typography color={colors.greenAccent[500]}>
                    {params.row.marketCap}$
                </Typography>
            ),
        },

        {
            field: "beta",
            headerName: "Beta",
            flex: 1,
            width:50

        },
        {
            field: "sector",
            headerName: "Sector",
            flex: 1,
            width:150
        }
    ];

    return (
        <Box m="20px">
            <Topbar title="STOCK SCREENER" subtitle="Search stocks based on criteria" ticker={'stockScreener'} isTicker={false}/>
            {
            <Box display="flex">
                <Select
                    options={stockScreenerFilters.marketCap}
                    defaultLabel={"Market cap Range"}
                    onSelect={(option) => setMarketCapRange(option)}
                    width={150}
                />
                <Select
                    options={stockScreenerFilters.price}
                    defaultLabel={"Price Range"}
                    onSelect={(option) => setPriceRange(option)}
                    width={120}
                />
                <Select
                    options={stockScreenerFilters.beta}
                    defaultLabel={"Beta Range"}
                    onSelect={(option) => setBetaRange(option)}
                    width={80}
                />
                <Select
                    options={stockScreenerFilters.volume}
                    defaultLabel={"Volume Range"}
                    onSelect={(option) => setVolumeRange(option)}
                    width={120}
                />
                <Select
                    options={stockScreenerFilters.dividends}
                    defaultLabel={"Dividend Range"}
                    onSelect={(option) => setDividendRange(option)}
                    width={80}
                />
                <Select
                    options={stockScreenerFilters.sector}
                    defaultLabel={"Sector"}
                    onSelect={(option) => {
                        setSector(option)
                    }}
                    width={150}
                />
                <Box
                    display="flex"
                    backgroundColor={colors.primary[400]}
                    borderRadius="3px"
                >
                    <InputBase sx={{ ml: 2, flex: 1 }} placeholder="Stock name" onChange={handleInputChange}/>
                    <IconButton type="button" sx={{ p: 1 }} onClick={searchStock}>
                        <SearchIcon />
                    </IconButton>
                </Box>
                <FormHelperText error={Boolean(error)}>{error}</FormHelperText>
            </Box>
            }
            <Box
                m="40px 0 0 0"
                height="75vh"
                sx={{
                    "& .MuiDataGrid-root": {
                        border: "none",
                    },
                    "& .MuiDataGrid-cell": {
                        borderBottom: "none",
                    },
                    "& .name-column--cell": {
                        color: colors.greenAccent[300],
                    },
                    "& .MuiDataGrid-columnHeaders": {
                        backgroundColor: colors.blueAccent[700],
                        borderBottom: "none",
                    },
                    "& .MuiDataGrid-virtualScroller": {
                        backgroundColor: colors.primary[400],
                    },
                    "& .MuiDataGrid-footerContainer": {
                        borderTop: "none",
                        backgroundColor: colors.blueAccent[700],
                    },
                    "& .MuiCheckbox-root": {
                        color: `${colors.greenAccent[200]} !important`,
                    },
                }}
            >
                <DataGrid rows={stocks} columns={columns} onRowClick={rowClickEvent}/>
            </Box>
        </Box>
    );
};

export default StockScreener;
