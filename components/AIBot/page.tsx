const AibotCard = ({ answer }: { answer?: string }) => {
    return (
      <div
      className={`min-w-96 w-fit md:ml-auto md:mr-auto text-gray-200 bg-slate-900 p-4 mt-10 rounded-lg flex justify-center`}
      >
        {answer == "" ? "Hello! How can I assist you?" : answer}
      </div>
    );
  };
  export default AibotCard;