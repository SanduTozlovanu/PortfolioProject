import {Box, Typography, useTheme} from "@mui/material";
import {DataGrid} from "@mui/x-data-grid";
import {tokens} from "../../theme";
import {mockDataStocks} from "../../data/mockData";
import Header from "../../components/Header";
import Select from "../../components/SelectComponent";

const StockScreener = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const columns = [
        {field: "id", headerName: "Id"},
        {field: "symbol", headerName: "Symbol"},
        {
            field: "marketCap",
            headerName: "Market Cap",
            flex: 1,
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
        },
        {
            field: "price",
            headerName: "Price",
            flex: 1,
            renderCell: (params) => (
                <Typography color={colors.greenAccent[500]}>
                    ${params.row.price}
                </Typography>
            ),
        },
        {
            field: "sector",
            headerName: "Sector",
            flex: 1,
        },
        {
            field: "industry",
            headerName: "Industry",
            flex: 1,
        },
    ];

    return (
        <Box m="20px">
            <Header title="STOCK SCREENER" subtitle="Search stocks based on criterias"/>

            {
            <Box display="flex">
                <Select
                    options={['Option 1', 'Option 2', 'Option 3']}
                    defaultLabel={"Market cap Range"}
                    onSelect={(option) => console.log(`Selected: ${option}`)}
                    width={150}
                />
                <Select
                    options={['Option 1', 'Option 2', 'Option 3']}
                    defaultLabel={"Price Range"}
                    onSelect={(option) => console.log(`Selected: ${option}`)}
                    width={120}
                />
                <Select
                    options={['Option 1', 'Option 2', 'Option 3']}
                    defaultLabel={"Beta Range"}
                    onSelect={(option) => console.log(`Selected: ${option}`)}
                    width={80}
                />
                <Select
                    options={['Option 1', 'Option 2', 'Option 3']}
                    defaultLabel={"Volume Range"}
                    onSelect={(option) => console.log(`Selected: ${option}`)}
                    width={120}
                />
                <Select
                    options={['Option 1', 'Option 2', 'Option 3']}
                    defaultLabel={"Dividend Range"}
                    onSelect={(option) => console.log(`Selected: ${option}`)}
                    width={80}
                />
                <Select
                    options={['Option 1', 'Option 2', 'Option 3']}
                    defaultLabel={"Sector"}
                    onSelect={(option) => console.log(`Selected: ${option}`)}
                    width={150}
                />
                <Select
                    options={['Option 1', 'Option 2', 'Option 3']}
                    defaultLabel={"Industry"}
                    onSelect={(option) => console.log(`Selected: ${option}`)}
                    width={150}
                />
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
                <DataGrid rows={mockDataStocks} columns={columns}/>
            </Box>
        </Box>
    );
};

export default StockScreener;
