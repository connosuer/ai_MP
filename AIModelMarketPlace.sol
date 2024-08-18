pragma solidity ^0.8.0;

contract AIModelMarketplace {
    struct Model {
        address owner;
        string name;
        string description;
        uint256 price;
        bool isAvailable;
        string ipfsHash;
        uint256 totalRating;
        uint256 numRatings;
    }

    mapping(uint256 => Model) public models;
    uint256 public modelCount;

    event ModelListed(uint256 indexed modelId, address indexed owner, string name, uint256 price, string ipfsHash);
    event ModelPurchased(uint256 indexed modelId, address indexed buyer, address indexed seller, uint256 price);
    event ModelUpdated(uint256 indexed modelId, string name, string description, uint256 price, string ipfsHash);
    event ModelRated(uint256 indexed modelId, address indexed rater, uint256 rating);

    function listModel(string memory _name, string memory _description, uint256 _price, string memory _ipfsHash) public {
        modelCount++;
        models[modelCount] = Model(msg.sender, _name, _description, _price, true, _ipfsHash, 0, 0);
        emit ModelListed(modelCount, msg.sender, _name, _price, _ipfsHash);
    }

    function purchaseModel(uint256 _modelId) public payable {
        Model storage model = models[_modelId];
        require(model.isAvailable, "Model is not available");
        require(msg.value >= model.price, "Insufficient payment");

        model.isAvailable = false;
        payable(model.owner).transfer(msg.value);

        emit ModelPurchased(_modelId, msg.sender, model.owner, msg.value);
    }

    function updateModel(uint256 _modelId, string memory _name, string memory _description, uint256 _price, string memory _ipfsHash) public {
        Model storage model = models[_modelId];
        require(msg.sender == model.owner, "Only the owner can update the model");

        model.name = _name;
        model.description = _description;
        model.price = _price;
        model.ipfsHash = _ipfsHash;

        emit ModelUpdated(_modelId, _name, _description, _price, _ipfsHash);
    }

    function rateModel(uint256 _modelId, uint256 _rating) public {
        require(_rating >= 1 && _rating <= 5, "Rating must be between 1 and 5");
        Model storage model = models[_modelId];
        model.totalRating += _rating;
        model.numRatings++;
        emit ModelRated(_modelId, msg.sender, _rating);
    }

    function getModelRating(uint256 _modelId) public view returns (uint256) {
        Model storage model = models[_modelId];
        if (model.numRatings == 0) return 0;
        return model.totalRating / model.numRatings;
    }
}