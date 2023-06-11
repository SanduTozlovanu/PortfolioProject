import {Box} from "@mui/material";
import Header from "../../components/Header";
import PieChart from "../../components/myPortfolio/PieChart";
import Topbar from "../global/Topbar";

const Pie = () => {
    return (
        <Box m="20px">
            <Topbar title="Pie Chart" subtitle="Portfolio Composition Pie Chart"
                    ticker={'PieChart'} isTicker={false}/>
            <Box height="75vh">
                <PieChart/>
            </Box>
        </Box>
    );
};

export default Pie;
