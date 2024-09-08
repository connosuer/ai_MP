pragma solidity ^0.8.0;

contract AIModelMarketplace {
    struct Model {
        string name;
        string description;
        address payable owner;
        uint256 price;
        bool isAvailable;
        string ipfsHash;
        uint256 totalRating;
        uint256 ratingCount;
    }

    mapping(uint256 => Model) public models;
    uint256 public modelCount;

    event ModelListed(uint256 indexed modelId, address indexed owner, string name, uint256 price);
    event ModelPurchased(uint256 indexed modelId, address indexed buyer, address indexed seller, uint256 price);
    event ModelRated(uint256 indexed modelId, address indexed rater, uint256 rating);

    function listModel(string memory _name, string memory _description, uint256 _price, string memory _ipfsHash) public {
        modelCount++;
        models[modelCount] = Model(_name, _description, payable(msg.sender), _price, true, _ipfsHash, 0, 0);
        emit ModelListed(modelCount, msg.sender, _name, _price);
    }

    function purchaseModel(uint256 _modelId) public payable {
        Model storage model = models[_modelId];
        require(model.isAvailable, "Model is not available");
        require(msg.value >= model.price, "Insufficient payment");

        model.isAvailable = false;
        model.owner.transfer(msg.value);

        emit ModelPurchased(_modelId, msg.sender, model.owner, msg.value);
    }

    function rateModel(uint256 _modelId, uint256 _rating) public {
        require(_rating >= 1 && _rating <= 5, "Rating must be between 1 and 5");
        Model storage model = models[_modelId];
        model.totalRating += _rating;
        model.ratingCount++;
        emit ModelRated(_modelId, msg.sender, _rating);
    }

    function getModel(uint256 _modelId) public view returns (string memory, string memory, address, uint256, bool, string memory) {
        Model storage model = models[_modelId];
        return (model.name, model.description, model.owner, model.price, model.isAvailable, model.ipfsHash);
    }

    function getModelRating(uint256 _modelId) public view returns (uint256) {
        Model storage model = models[_modelId];
        if (model.ratingCount == 0) return 0;
        return model.totalRating / model.ratingCount;
    }

    function getModelCount() public view returns (uint256) {
        return modelCount;
    }
}