import AskQuestion from "./components/AskQuestion";
import UploadDocument from "./components/UploadDocument";
import ProposalScoring from "./components/ProposalScoring";

export default function App() {
  return (
    <div className="app">
      <h1>BidIntel</h1>
      <UploadDocument />
      <AskQuestion opportunityId="dhs-cyber" />
      <ProposalScoring opportunityId="dhs-cyber" />
    </div>
  );
}
